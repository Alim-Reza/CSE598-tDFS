# from src.custom_tensor import CustomTensor
# from src.utils.video_processor import load_video_chunk
from src.pickle_tensor import PickleTensor
import os

def main():
    import time
    start_time = time.time()
    print(f"\nExecution time start: {start_time:.2f} seconds")
    
    directory = os.path.join('data', 'processed', 'video_chunks')
    target_shape = (100, 360, 640, 3)

    order_func = lambda x: int(x.split('_')[-1].split('.')[0])
    
    # Modified transform function to verify data
    def transform_func(x):
        frames = [frame.astype('float32') / 255.0 for frame in x]
        # Verify data isn't all zeros
        # if len(frames) > 0:
        #     print(f"Sample values from first frame:")
        #     print(f"Min: {frames[0].min()}, Max: {frames[0].max()}, Mean: {frames[0].mean()}")
        return frames

    tensor = PickleTensor.load_from_pickles(
        directory=directory,
        target_shape=target_shape,
        order_by=order_func,
        transform=transform_func
    )

    def slice_printing(tensor):
        # After loading the tensor, add these slicing examples
        print("\nAdvanced slicing examples:")
        
        # Get every other frame from first 10 frames
        print("Every other frame shape:", tensor[:10:2].shape)
        
        # Get center crop of all frames
        center_crop = tensor[:, 90:270, 160:480]
        print("Center crop shape:", center_crop.shape)
        
        # Get specific color channel for all frames
        red_channel = tensor[..., 0]  # Using ellipsis notation
        print("All red channels shape:", red_channel.shape)
        
        # Multiple dimension slicing
        subset = tensor[10:20, ::2, ::2]  # frames 10-20, every 2nd pixel
        print("Subsampled frames shape:", subset.shape)
        
        # Boolean indexing
        bright_pixels = tensor > 0.5
        print("Bright pixels mask shape:", bright_pixels.shape)
        
        # Fancy indexing
        specific_frames = tensor[[0, 5, 10, 15]]  # Get specific frames
        print("Selected frames shape:", specific_frames.shape)


    slice_printing(tensor)
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

     # Add at the very end of main(), before the if __name__ == "__main__":
    end_time = time.time()
    print(f"\nExecution time ends: {end_time:.2f} seconds")
    print(f"\n======================> Execution time: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()