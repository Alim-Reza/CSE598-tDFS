import imageio.v3 as iio
import pickle
import os

def chunk_video_to_pickles(video_path, output_dir, frames_per_chunk=100):
    """
    Split video into multiple pickle files, each containing a specific number of frames
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load video using imageio
    with iio.imopen(video_path, 'r', plugin='pyav') as file:
        metadata = file.metadata()
        fps = metadata.get('fps', 30)  # default to 30 if not found
        frames = list(file.read())  # read all frames
        total_frames = len(frames)
    
    chunk_number = 0
    frame_count = 0
    
    # Process frames in chunks
    for i in range(0, total_frames, frames_per_chunk):
        chunk_frames = frames[i:i + frames_per_chunk]
        chunk_data = {
            'frames': chunk_frames,
            'fps': fps,
            'chunk_number': chunk_number,
            'start_frame': i
        }
        
        chunk_path = os.path.join(output_dir, f'video_chunk_{chunk_number}.pkl')
        with open(chunk_path, 'wb') as f:
            pickle.dump(chunk_data, f)
        
        frame_count += len(chunk_frames)
        chunk_number += 1
    
    # Save metadata
    metadata = {
        'total_frames': frame_count,
        'fps': fps,
        'frames_per_chunk': frames_per_chunk,
        'total_chunks': chunk_number
    }
    
    with open(os.path.join(output_dir, 'video_metadata.pkl'), 'wb') as f:
        pickle.dump(metadata, f)

def load_video_chunk(chunk_path):
    """
    Load a specific chunk of the video
    """
    with open(chunk_path, 'rb') as f:
        return pickle.load(f)

# Example usage
video_path = 'E:\\CSE598-tDFS\\code\\data\\raw\\videos\\main_video.mp4'
chunks_dir = 'E:\\CSE598-tDFS\\code\\data\\processed\\video_chunks'

# Split video into chunks of 100 frames each
chunk_video_to_pickles(video_path, chunks_dir, frames_per_chunk=100)

# Load a specific chunk (e.g., chunk 0)
chunk_data = load_video_chunk(os.path.join(chunks_dir, 'video_chunk_0.pkl'))