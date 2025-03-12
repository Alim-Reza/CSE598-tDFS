from src.custom_tensor import CustomTensor
from src.utils.video_processing import load_video_chunk
import os

def main():
    # Path to processed video chunks
    # chunks_dir = os.path.join('data', 'processed', 'video_chunks')
    
    # # Load a video chunk
    # chunk_data = load_video_chunk(os.path.join(chunks_dir, 'video_chunk_0.pkl'))
    
    # # Convert frames to CustomTensor
    # frames_tensor = CustomTensor(chunk_data['frames'])
    
    # # Now you can use your tensor operations
    # print(f"Video chunk shape: {frames_tensor.shape}")
    # print(f"Frame mean: {frames_tensor.mean()}")

if __name__ == "__main__":
    main()