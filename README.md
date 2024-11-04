
# Video Conversion Script

This project is a Python script for converting video files to a specific format with optional bitrate adjustment, upscaling, and metadata removal. The script automatically detects the available GPU (NVIDIA, AMD, or CPU) to select the appropriate video encoder, making the conversion process more efficient.

## Features

- **Automatic GPU Detection**: Detects NVIDIA or AMD GPUs (or defaults to CPU if no GPU is found) and selects the best encoder.
- **Batch Conversion**: Processes all videos in the specified directory that match the given input formats.
- **Bitrate Adjustment**: Option to specify a target bitrate, or default to the original bitrate.
- **Upscaling**: Option to upscale the video to a specified resolution.
- **Metadata Removal**: Option to remove metadata from the video.
- **Progress Tracking**: Displays a progress bar for each file and the overall process using `tqdm`.

## Requirements

- Python 3 or higher
- [FFmpeg](https://ffmpeg.org/download.html) installed and accessible from the command line
- `tqdm` Python package for displaying progress bars

## Installation

### 1. Install FFmpeg

FFmpeg is required for video processing. You can install it via:

- **Windows**: Download the FFmpeg executable from [FFmpeg's website](https://ffmpeg.org/download.html) and add it to your PATH.
- **Linux (Debian/Ubuntu)**:
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```
- **macOS**:
  ```bash
  brew install ffmpeg
  ```

### 2. Install `tqdm`

To install `tqdm` for progress bars, run:
```bash
pip install tqdm
```

## Usage

To run the script, use the command below, replacing the placeholders with your own values:

```bash
python video_converter.py -d <directory_path> -i .mp4 .avi -o .mkv -b 600k -r 1280x720 --remove_metadata
```

### Arguments

| Argument              | Description                                                                                      |
|-----------------------|--------------------------------------------------------------------------------------------------|
| `-d`, `--directory`   | Directory where the videos are located. **Required**                                             |
| `-i`, `--input_formats` | Input formats for the files to be converted (e.g., `.mp4 .ts`). If none are provided, all video files in the directory will be converted. |
| `-o`, `--output_format` | Output format for the converted files (default: `.mkv`).                                        |
| `-b`, `--bitrate`     | Bitrate for the video (e.g., `600k`). If not provided, the original bitrate is used.             |
| `-r`, `--resolution`  | Resolution for upscaling (e.g., `1280x720`). If not provided, no upscaling is applied.           |
| `--remove_metadata`   | Option to remove metadata from the video file.                                                   |

### Example Usage

```bash
python video_converter.py -d ./videos -i .mp4 -o .mkv -b 800k -r 1920x1080 --remove_metadata
```

This example will:
1. Look for `.mp4` files in the `./videos` directory.
2. Convert them to `.mkv` format with a bitrate of 800k and a resolution of 1920x1080.
3. Remove any metadata from the video files.

## How the Script Works

1. **GPU Detection**: The script detects whether a GPU is available and selects the appropriate encoder:
   - If an NVIDIA GPU is detected, it uses the `hevc_nvenc` encoder.
   - If an AMD GPU is detected, it uses the `hevc_amf` encoder.
   - If no GPU is detected, it defaults to the `libx265` encoder for CPU-based encoding.

2. **Batch Processing**: The script goes through all files in the specified directory. If `--input_formats` is specified, it only processes files that match those formats.

3. **Conversion Process**:
   - **Original Files**: Each original file is moved to an `old` subdirectory in the specified directory before conversion.
   - **Conversion Command**: The script builds an FFmpeg command with the selected options (encoder, bitrate, resolution, metadata removal).
   - **Progress Display**: A progress bar shows the overall progress, while each file's individual progress is also tracked.

4. **Output**: The converted files are saved in the same directory with the specified output format, leaving the original files in the `old` subdirectory.

## Additional Notes

- Make sure `ffmpeg` and `ffprobe` are available in your PATH, as they are essential for this script.
- `tqdm` will provide visual feedback for progress; ensure your terminal supports this display.
- Test on a small batch first to confirm that your parameters (bitrate, resolution, etc.) provide the desired output quality.

Happy converting!
