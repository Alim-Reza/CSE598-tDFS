import torch
import os
import pickle
import numpy as np
from typing import Callable, Tuple, Optional

class PickleTensor(torch.Tensor):
    def __new__(cls, *args, **kwargs):
        return super(PickleTensor, cls).__new__(cls, *args, **kwargs)

    @staticmethod
    def load_from_pickles(
        directory: str,
        target_shape: Tuple[int, ...],
        order_by: Callable = lambda x: x,
        transform: Callable = lambda x: x
    ) -> 'PickleTensor':
        # Get and sort pickle files
        pickle_files = [f for f in os.listdir(directory) 
                       if f.endswith('.pkl') and f.startswith('video_chunk_')]
        pickle_files.sort(key=order_by)
        
        # Pre-allocate tensor with correct shape and dtype
        result = torch.empty(target_shape, dtype=torch.float32)
        
        # Process files one at a time
        current_frame = 0
        for pickle_file in pickle_files:
            with open(os.path.join(directory, pickle_file), 'rb') as f:
                data = pickle.load(f)
                if 'frames' in data:
                    frames = data['frames']
                    # Transform frames one at a time
                    for frame in frames:
                        if current_frame >= target_shape[0]:
                            break
                        # Process single frame
                        processed_frame = transform([frame])[0]
                        result[current_frame] = torch.from_numpy(processed_frame)
                        current_frame += 1
        
        return PickleTensor(result)

    @classmethod
    def __torch_function__(cls, func, types, args=(), kwargs=None):
        if kwargs is None:
            kwargs = {}
        return super().__torch_function__(func, types, args, kwargs)