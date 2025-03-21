# Video Tensor Processing System

A Python-based system for efficient video processing and tensor manipulation, built on PyTorch.

## System Requirements

- Windows 10/11
- Python 3.8+
- CUDA-compatible GPU (optional)
- 8GB RAM minimum

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alim-reza/CSE598-tDFS.git
cd CSE598-tDFS```

2. Install dependencies:
```pip install -r requirements.txt```

## Project Structure

```CSE598-tDFS/
├── config/
│   └── paths.py          # Centralized path configuration
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
└── main.py              # Main execution script```