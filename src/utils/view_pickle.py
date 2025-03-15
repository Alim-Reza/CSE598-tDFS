import pickle
import os
import cv2
import numpy as np

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
            if frames:
                print(f"First frame type: {type(frames[0])}")
                if hasattr(frames[0], 'shape'):
                    print(f"First frame shape: {frames[0].shape}")
                
                while True:
                    frame_idx = input("\nEnter frame number (0-{}) or 'q' to quit: ".format(len(frames)-1))
                    if frame_idx.lower() == 'q':
                        break
                    
                    try:
                        idx = int(frame_idx)
                        if 0 <= idx < len(frames):
                            frame = frames[idx]
                            while True:
                                view_type = input("\nView as (1) Image or (2) Array data or (b) Back: ")
                                
                                if view_type == '1':
                                    cv2.imshow(f'Frame {idx}', frame)
                                    cv2.waitKey(0)
                                    cv2.destroyAllWindows()
                                elif view_type == '2':
                                    print(f"\nFrame {idx} data:")
                                    print(f"Array shape: {frame.shape}")
                                    print(f"Data type: {frame.dtype}")
                                    print(f"Min value: {np.min(frame)}")
                                    print(f"Max value: {np.max(frame)}")
                                    print(f"Mean value: {np.mean(frame)}")
                                    
                                    # Show a sample from different parts of the array
                                    print("\nSample values from different parts of the array:")
                                    h, w = frame.shape[:2]
                                    print(f"Top-left corner (5x5):\n{frame[:5, :5]}")
                                    print(f"\nCenter (5x5):\n{frame[h//2-2:h//2+3, w//2-2:w//2+3]}")
                                    
                                    view_full = input("\nView full array? (y/n): ")
                                    if view_full.lower() == 'y':
                                        np.set_printoptions(threshold=np.inf)
                                        print("\nFull array:")
                                        print(frame)
                                        np.set_printoptions(threshold=1000)
                                elif view_type.lower() == 'b':
                                    break
                                else:
                                    print("Invalid option!")
                        else:
                            print("Invalid frame index!")
                    except ValueError:
                        print("Please enter a valid number or 'q'")
    
    # Print other metadata if exists
    for key in data:
        if key != 'frames':
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