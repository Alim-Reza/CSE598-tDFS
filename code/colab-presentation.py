import torch
import os
import pickle
import numpy as np
from typing import Callable, Tuple, Optional, List
import concurrent.futures
import lzma
import requests

def decompress_and_load(data_tuple):
    """Helper function to decompress and load pickle data"""
    file_name, content = data_tuple
    try:
        decompressed = lzma.decompress(content)
        return pickle.loads(decompressed)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        return None

class PickleTensor(torch.Tensor):
    # ... existing __new__ and other methods ...

    def slice_to_pickle_files(self, slice_obj) -> List[str]:
        """Convert a slice to required pickle file names"""
        start = slice_obj.start if slice_obj.start is not None else 0
        stop = slice_obj.stop if slice_obj.stop is not None else self.shape[0]
        
        start_pickle = start // 100
        end_pickle = (stop - 1) // 100
        
        return [f"video_chunk_{i}.pkl.xz" for i in range(start_pickle, end_pickle + 1)]

    def load_slice_data(self, slice_obj: slice, transform_func: Optional[Callable] = None,
                       hdfs_config: dict = None) -> torch.Tensor:
        """Load specific frames from HDFS based on slice"""
        if hdfs_config is None:
            raise ValueError("HDFS configuration required")

        files_to_fetch = self.slice_to_pickle_files(slice_obj)
        print(f"\nPreparing to download {len(files_to_fetch)} files:")
        for f in files_to_fetch:
            print(f"  - {f}")


        # Download and decompress using ThreadPoolExecutor
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Download files
            futures = []
            for file_name in files_to_fetch:
                print(f"\nStarting download: {file_name}")
                url = f"http://{hdfs_config['host']}:{hdfs_config['port']}/webhdfs/v1{hdfs_config['base_path']}/{file_name}?op=OPEN&user.name=hdfs"
                futures.append(executor.submit(requests.get, url, stream=True, timeout=30))
            
            downloaded_data = []
            for future, file_name in zip(futures, files_to_fetch):
                try:
                    response = future.result()
                    response.raise_for_status()
                    downloaded_data.append((file_name, response.content))
                    print(f"Successfully downloaded: {file_name}")
                except Exception as e:
                    print(f"Error downloading {file_name}: {e}")

            # Decompress files
            futures = [executor.submit(decompress_and_load, data) for data in downloaded_data]
            pickle_data = []
            for future in futures:
                result = future.result()
                if result is not None:
                    pickle_data.append(result)

        # Extract required frames
        start_frame = slice_obj.start if slice_obj.start is not None else 0
        start_offset = start_frame % 100
        frames_needed = slice_obj.stop - start_frame if slice_obj.stop is not None else self.shape[0] - start_frame

        # Collect frames
        all_frames = []
        frames_collected = 0

        for data in pickle_data:
            if frames_collected >= frames_needed:
                break

            frames = data['frames']
            if data['chunk_number'] == start_frame // 100:
                frames = frames[start_offset:]

            remaining = frames_needed - frames_collected
            frames = frames[:remaining]

            if transform_func:
                frames = transform_func(frames)

            all_frames.extend(frames)
            frames_collected += len(frames)

        # Convert to tensor
        return torch.from_numpy(np.array(all_frames))


        
config = {
    'host': '160.191.162.36',
    'port': 9870,
    'base_path': '/user/pickles'
}
# target_shape = (500, 360, 640, 3)  
tensor = PickleTensor()

frames = tensor.load_slice_data(
    slice(50, 450),
    transform_func=lambda x: [frame.astype('float32') / 255.0 for frame in x],
    hdfs_config=config
)