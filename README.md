# Video Tensor Processing System

A Python-based system for efficient video processing and tensor manipulation, built on PyTorch.

The colab file for the project is here:
[distributed_file_load_for_tensor.ipynb](https://github.com/Alim-Reza/CSE598-tDFS/blob/custom-tensor/code/distributed_file_load_for_tensor.ipynb)
## System Requirements

- Windows 10/11
- Python 3.8+
- 8GB RAM minimum

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alim-reza/CSE598-tDFS.git
cd CSE598-tDFS
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```bash
CSE598-tDFS/
├── config/
│   └── paths.py          # Centralized path configuration, TODO: Not done yet
├── src/
│   ├── utils/
│   │   ├── __init__.py
│   │   └── video_processor.py  # Video processing utilities
│   ├── __init__.py
│   └── pickle_tensor.py  # Custom PyTorch tensor implementation
├── data/
│   ├── raw/
│   │   └── videos/      # Place input videos here
│   └── processed/
│       └── video_chunks/ # Processed pickle files
└── main.py              # Main execution script
```

## Command for running:
1. For generating the pickle files
```bash
python .\code\src\utils\video_processor.py
```

make sure to update the file path with ur own directory name, on the video_processor.py
```
video_path = 'E:\\CSE598-tDFS\\code\\data\\raw\\videos\\main_video.mp4'
chunks_dir = 'E:\\CSE598-tDFS\\code\\data\\processed\\video_chunks'
```
2. For viewing the pickle file : (can be viewed by both image and array file)
```bash
python .\code\src\utils\view_pickle.py
```
3. For seeing  the PickleTensor class in action:
```bash
cd code
python main.py
```

4. For testing the PickleTensor class with the actual PyTorch Tensor class:
```bash
cd code
python -m unittest .\tests\test_tensor_comparison.py
```

