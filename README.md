# Video Converter with FFmpeg

This project provides a command-line utility to convert video files to a specific format with optional upscaling, bitrate adjustment, and metadata removal. It leverages FFmpeg for the conversion process and automatically detects the GPU type (NVIDIA, AMD, or CPU) to use the optimal encoder.

## Features

- Converts video files to a specified format (e.g., MKV).
- Automatically detects available GPU to use the most suitable encoder (NVIDIA, AMD, or CPU).
- Option to adjust the resolution of the output video.
- Option to remove metadata from video files.
- Option to specify a custom bitrate.
- Parallel processing of multiple video files for efficiency.

## Prerequisites

- Python 3.12+
- FFmpeg installed and available in the system's PATH.
- NVIDIA or AMD GPU drivers installed if available (optional).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/brunormorillo/video-converter.git
   cd video-converter
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

   The required packages are:

   - `tqdm`: For progress visualization.

## Usage

To run the video conversion script, use the following command:

```bash
python convert.py -d <directory> [options]
```

### Arguments and Options

- **`-d`, `--directory`** (required): Directory where the videos are located.

  Example: `-d /path/to/videos`

- **`-i`, `--input_formats`** (optional): Input formats of the files to be converted (e.g., `.mp4 .ts`). If not provided, all video files in the directory will be converted.

  Example: `-i .mp4 .avi`

- **`-o`, `--output_format`** (optional): Output format of the converted files (default: `.mkv`).

  Example: `-o .mp4`

- **`-b`, `--bitrate`** (optional): Bitrate for the video (e.g., `600k`). If not provided, the original bitrate is used.

  Example: `-b 800k`

- **`-r`, `--resolution`** (optional): Resolution for upscaling (e.g., `1280x720`). If not provided, no upscaling is applied.

  Example: `-r 1920x1080`

- **`--remove_metadata`** (optional): Remove metadata from the video file.

  Example: `--remove_metadata`

### Examples

1. Convert all video files in a directory to MKV format with the original bitrate:

   ```bash
   python video_converter.py -d /path/to/videos
   ```

2. Convert only `.mp4` and `.avi` files to `.mkv`, upscale to `1280x720`, and remove metadata:

   ```bash
   python video_converter.py -d /path/to/videos -i .mp4 .avi -r 1280x720 --remove_metadata
   ```

3. Convert all video files to `.mp4` format with a custom bitrate of `800k`:
   ```bash
   python video_converter.py -d /path/to/videos -o .mp4 -b 800k
   ```

## How It Works

1. The script detects the type of GPU available (NVIDIA, AMD, or CPU) and selects the appropriate encoder.
2. It collects all the video files that match the input formats specified.
3. It creates an "old" directory in the provided directory to store the original files.
4. It processes each video using FFmpeg with options like bitrate, resolution, and metadata removal based on user input.
5. The processing is done in parallel using multiple threads to speed up the conversion of large batches of files.

## Handling Errors

- If FFmpeg is not found in the system's PATH, the script will notify the user.
- If any conversion fails, the original file is restored to its initial location.

## Notes

- Ensure that FFmpeg is installed and accessible from your command line before running the script. You can install FFmpeg using:
  - **Ubuntu**: `sudo apt-get install ffmpeg`
  - **Windows**: Download from [FFmpeg's official website](https://ffmpeg.org/download.html).

## Contributing

Feel free to submit pull requests or issues to improve this project. Contributions are welcome!

## License

This project is licensed under the MIT License.

## Acknowledgments

- Thanks to the developers of [FFmpeg](https://ffmpeg.org/) for creating a versatile tool for multimedia processing.
