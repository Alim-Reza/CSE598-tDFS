
# Video Tensor Processing System with Redis Caching

A system for efficient video data processing and analysis using tensor operations with Redis caching integration.

## Features

- Video data processing with tensor operations
- Redis caching for improved performance
- Advanced tensor operations including:
  - Frame selection and slicing 
  - Center cropping
  - Color channel extraction
  - Multi-dimensional operations
  - Boolean indexing
- Performance monitoring and statistics

## Installation

### Prerequisites
- Python 3.8+
- Redis server
- Required Python packages

### Setup Redis (Windows)
option 1:
    1. Download Memurai (Redis for Windows) from https://www.memurai.com/get-memurai
    2. Run installer and follow setup wizard
    3. Memurai will run automatically as a Windows service
option 2:
# Using WSL (Windows Subsystem for Linux)
# Enable WSL and install Redis through Ubuntu
   1. Open PowerShell as Administrator
   2. Run `wsl --install` to install WSL
   3. Open Ubuntu from the Start menu
   4. Run `sudo apt-get update`
   5. Run `sudo apt-get install redis-server`
   6. Start Redis server: `sudo service redis-server start`
   7. Verify Redis server is running: `redis-cli ping`

### Setup Redis (Linux)
1. Update package list: `sudo apt-get update`   
2. Install Redis: `sudo apt-get install redis-server`
3. Start Redis server: `sudo service redis-server start`
4. Verify Redis server is running: `redis-cli ping`

### Setup Redis (Mac)
1. Install Homebrew: `/bin/bash -c "$(curl -fsSL
2. Install Redis: `sudo apt-get install redis-server`   
3. Start Redis server: `sudo service redis-server start` 
4. Verify Redis server is running: `redis-cli ping`

### Install Python Dependencies
```bash
pip install redis numpy pickle-mixin
```

### Project Setup
```bash
# Clone repository
git clone <your-repo-url>
cd CSE598-tDFS

# Create required directories
mkdir -p data/processed/video_chunks
```

## Project Structure
```
CSE598-tDFS/
├── code/
│   ├── main.py              # Main application
│   └── src/
│       ├── pickle_tensor.py # Tensor operations
│       └── redis_handler.py # Redis caching
├── data/
│   └── processed/
│       └── video_chunks/    # Video data
└── README.md
```

## Usage

1. Ensure Redis server is running
2. Place video chunks in `data/processed/video_chunks/`
3. Run the application:
```bash
python code/main.py
```

## Tensor Operations Examples

```python
# Load tensor
tensor = PickleTensor.load_from_pickles(directory, target_shape)

# Basic operations
first_frame = tensor[0]                    # Single frame
first_5_frames = tensor[:5]                # Multiple frames
center_crop = tensor[:, 90:270, 160:480]   # Spatial cropping

# Advanced operations
red_channel = tensor[..., 0]               # Color channel
subsampled = tensor[10:20, ::2, ::2]       # Subsampling
bright_areas = tensor > 0.5                # Boolean indexing
```

## Configuration

Default settings:
- Frame dimensions: 360x640x3 (HxWxRGB)
- Chunk size: 100 frames
- Redis port: 6379
- Redis host: localhost

## Troubleshooting

Common issues:

1. Redis Connection Failed
   - Check if Redis service is running
   - Verify port 6379 is available
   - Ensure Redis is properly installed

2. Memory Issues
   - Reduce chunk size in main.py
   - Adjust Redis memory settings
   - Monitor system resources

## Contributing

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Submit pull request

