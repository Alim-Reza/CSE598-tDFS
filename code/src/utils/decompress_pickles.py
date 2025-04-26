import lzma
import pickle
import os
from pathlib import Path

def decompress_single_file(input_path, output_path=None):
    """Decompress a single LZMA compressed pickle file"""
    if output_path is None:
        output_path = input_path[:-3] if input_path.endswith('.xz') else input_path + '_decompressed'
    
    with open(input_path, 'rb') as f:
        compressed_data = f.read()
    
    # Decompress with LZMA
    decompressed_data = lzma.decompress(compressed_data)
    
    with open(output_path, 'wb') as f:
        f.write(decompressed_data)
    
    return output_path

# Example usage:
if __name__ == "__main__":
    # Compress single file
    file_path = "data/processed/video_chunks/chunk_1.pkl"
    # compressed_file = compress_single_file(file_path)
    
    # Decompress single file
    decompressed_file = decompress_single_file(compressed_file)

# Modified PickleTensor to handle compressed files
def load_compressed_pickle(file_path):
    """Load a compressed pickle file"""
    with open(file_path, 'rb') as f:
        if file_path.endswith('.xz'):
            return pickle.loads(lzma.decompress(f.read()))
        return pickle.load(f)