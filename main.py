from src.custom_tensor import CustomTensor
from src.utils.video_processor import load_video_chunk
import os

def process_video_chunks(
    directory: str = os.path.join('data', 'processed', 'video_chunks'),
    shape_filter: tuple = None,
    order_by: callable = lambda x: x,
    transform: callable = lambda x: x
) -> list:
    processed_tensors = []
    
    # Get all pickle files in directory and filter for video chunks only
    pickle_files = [
        f for f in os.listdir(directory) 
        if f.endswith('.pkl') and f.startswith('video_chunk_')
    ]
    
    # Sort files based on order_by function
    pickle_files.sort(key=order_by)
    
    for pickle_file in pickle_files:
        chunk_data = load_video_chunk(os.path.join(directory, pickle_file))
        tensor = CustomTensor(chunk_data['frames'])
        
        # Apply shape filter if specified
        if shape_filter and tensor.shape != shape_filter:
            continue
            
        # Apply transformation
        transformed_tensor = transform(tensor)
        processed_tensors.append(transformed_tensor)
    
    return processed_tensors

def main():
    # chunks_dir = os.path.join('data', 'processed', 'video_chunks')
    
    # print(f"Looking for chunks in: {chunks_dir}")
    
    # if not os.path.exists(chunks_dir):
    #     print(f"Error: Directory {chunks_dir} does not exist")
    #     return
    
    # # First, let's check the shape of the first chunk without filtering
    # sample_data = process_video_chunks(
    #     directory=chunks_dir,
    #     shape_filter=None,  # No shape filter for this check
    #     order_by=lambda x: int(x.split('_')[-1].split('.')[0])
    # )
    
    # if sample_data:
    #     actual_shape = sample_data[0].shape
    #     print(f"Detected tensor shape: {actual_shape}")
        
    #     # Now process with the correct shape
    #     processed_data = process_video_chunks(
    #         directory=chunks_dir,
    #         shape_filter=actual_shape,
    #         order_by=lambda x: int(x.split('_')[-1].split('.')[0]),
    #         transform=lambda x: x
    #     )
        
    #     print(f"Type of processed_data: {type(processed_data)}")
    #     print(f"Length of processed_data: {len(processed_data)}")
        
    #     if processed_data:
    #         print(f"Processed {len(processed_data)} chunks")
    #         print(f"First chunk shape: {processed_data[0].shape}")
    # else:
    #     print("No chunks were found in the directory")

    

if __name__ == "__main__":
    main()