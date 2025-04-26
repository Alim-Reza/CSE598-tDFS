import lzma
import pickle
import os
from pathlib import Path
import multiprocessing
import time
from concurrent.futures import ProcessPoolExecutor

def list_available_chunks(directory):
    """List all available pickle files in the directory"""
    files = [f for f in os.listdir(directory) if f.endswith('.pkl')]
    if not files:
        print(f"No .pkl files found in {directory}")
        return None
    print("\nAvailable chunks:")
    for i, f in enumerate(files):
        print(f"{i}: {f}")
    return files

def compress_single_file(input_path, output_path=None):
    """Compress a single pickle file using LZMA compression"""
    start_time = time.time()
    if output_path is None:
        output_path = input_path + '.xz'
    
    with open(input_path, 'rb') as f:
        data = f.read()
    
    compressed_data = lzma.compress(data, preset=9)
    
    with open(output_path, 'wb') as f:
        f.write(compressed_data)
    
    original_size = os.path.getsize(input_path)
    compressed_size = os.path.getsize(output_path)
    elapsed_time = time.time() - start_time
    return (input_path, original_size, compressed_size, elapsed_time)

def compress_parallel(file_list, chunks_dir):
    """Compress multiple files in parallel"""
    with ProcessPoolExecutor() as executor:
        futures = []
        for f in file_list:
            file_path = str(chunks_dir / f)
            futures.append(executor.submit(compress_single_file, file_path))
        
        # Process results as they complete
        for future in futures:
            input_path, orig_size, comp_size, elapsed = future.result()
            print(f"Compressed {os.path.basename(input_path)}: "
                  f"{orig_size/1024:.2f}KB -> {comp_size/1024:.2f}KB "
                  f"in {elapsed:.2f} seconds")

def load_compressed_pickle(file_path):
    """Load a compressed pickle file"""
    with open(file_path, 'rb') as f:
        if file_path.endswith('.xz'):
            return pickle.loads(lzma.decompress(f.read()))
        return pickle.load(f)

if __name__ == "__main__":
    # Get the project root directory
    project_root = Path("E:\\CSE598-tDFS")
    chunks_dir = project_root / "code" / "data" / "processed" / "video_chunks"
    
    # List available chunks
    files = list_available_chunks(chunks_dir)
    if files:
        start_time = time.time()
        compress_parallel(files, chunks_dir)
        total_time = time.time() - start_time
        print(f"\nTotal compression time: {total_time:.2f} seconds")