import pickle
import os

def view_pickle_content(pickle_path):
    with open(pickle_path, 'rb') as f:
        data = pickle.load(f)
    
    print("Pickle File Contents:")
    print("-" * 50)
    print(f"Keys in the dictionary: {list(data.keys())}")
    
    if 'frames' in data:
        frames = data['frames']
        if isinstance(frames, list):
            print(f"\nFrames is a list with length: {len(frames)}")
            if frames:  # If list is not empty
                print(f"First frame type: {type(frames[0])}")
                if hasattr(frames[0], 'shape'):
                    print(f"First frame shape: {frames[0].shape}")
        else:
            print(f"\nFrames shape: {frames.shape}")
            print(f"Frames dtype: {frames.dtype}")
    
    # Print other metadata if exists
    for key in data:
        if key != 'frames':  # Skip frames as we already showed its info
            print(f"\n{key}: {data[key]}")

if __name__ == "__main__":
    chunks_dir = os.path.join('data', 'processed', 'video_chunks')
    
    # List all pickle files
    pickle_files = [f for f in os.listdir(chunks_dir) if f.endswith('.pkl')]
    
    print("Available pickle files:")
    for i, file in enumerate(pickle_files):
        print(f"{i}: {file}")
    
    # Let user select which file to view
    file_idx = int(input("\nEnter the number of the file you want to view: "))
    pickle_path = os.path.join(chunks_dir, pickle_files[file_idx])
    
    view_pickle_content(pickle_path)