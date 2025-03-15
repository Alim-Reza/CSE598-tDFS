from src.custom_tensor import CustomTensor
from src.utils.video_processor import load_video_chunk
from src.pickle_tensor import PickleTensor
import os

# def process_video_chunks(
#     directory: str = os.path.join('data', 'processed', 'video_chunks'),
#     shape_filter: tuple = None,
#     order_by: callable = lambda x: x,
#     transform: callable = lambda x: x
# ) -> list:
    # processed_tensors = []
    
    # # Get all pickle files in directory and filter for video chunks only
    # pickle_files = [
    #     f for f in os.listdir(directory) 
    #     if f.endswith('.pkl') and f.startswith('video_chunk_')
    # ]
    
    # # Sort files based on order_by function
    # pickle_files.sort(key=order_by)
    
    # for pickle_file in pickle_files:
    #     chunk_data = load_video_chunk(os.path.join(directory, pickle_file))
    #     tensor = CustomTensor(chunk_data['frames'])
        
    #     # Apply shape filter if specified
    #     if shape_filter and tensor.shape != shape_filter:
    #         continue
            
    #     # Apply transformation
    #     transformed_tensor = transform(tensor)
    #     processed_tensors.append(transformed_tensor)
    
    # return processed_tensors

def main():
    directory = os.path.join('data', 'processed', 'video_chunks')
    target_shape = (100, 360, 640, 3)

    order_func = lambda x: int(x.split('_')[-1].split('.')[0])
    
    # Modified transform function to verify data
    def transform_func(x):
        frames = [frame.astype('float32') / 255.0 for frame in x]
        # Verify data isn't all zeros
        if len(frames) > 0:
            print(f"Sample values from first frame:")
            print(f"Min: {frames[0].min()}, Max: {frames[0].max()}, Mean: {frames[0].mean()}")
        return frames

    tensor = PickleTensor.load_from_pickles(
        directory=directory,
        target_shape=target_shape,
        order_by=order_func,
        transform=transform_func
    )

    # Print more detailed information about the tensor
    print("\nTensor statistics:")
    print(f"Min value: {tensor.min().item()}")
    print(f"Max value: {tensor.max().item()}")
    print(f"Mean value: {tensor.mean().item()}")
    
    # View a specific region with values
    print("\nSample 5x5 region from first frame:")
    print(tensor[0, 100:105, 100:105, 0])  # Red channel sample
    
    # Example slicing operations
    print("\nTensor slicing examples:")
    print(f"Full tensor shape: {tensor.shape}")
    
    # Get first frame
    print("\nFirst frame shape:", tensor[0].shape)
    
    # Get first 5 frames
    print("\nFirst 5 frames shape:", tensor[:5].shape)
    
    # Get a specific region of a frame (middle portion)
    middle_region = tensor[0, 150:210, 270:370]
    print("\nMiddle region shape:", middle_region.shape)
    
    # Get RGB channels of first frame
    print("\nRed channel of first frame:", tensor[0, :, :, 0])
    print("Green channel of first frame:", tensor[0, :, :, 1])
    print("Blue channel of first frame:", tensor[0, :, :, 2])

if __name__ == "__main__":
    main()