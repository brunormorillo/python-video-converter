# Video Converter with FFmpeg

This project provides a command-line utility to convert video files to a specific format with optional upscaling, bitrate adjustment, metadata removal, and more. It leverages FFmpeg for the conversion process and automatically detects the GPU type (NVIDIA, AMD, or CPU) to use the optimal encoder.

## Features

- Converts video files to a specified format (e.g., MKV).
- Automatically detects available GPU to use the most suitable encoder (NVIDIA, AMD, or CPU).
- Option to adjust the resolution of the output video.
- Option to remove metadata from video files.
- Option to specify a custom bitrate for video and audio.
- Option to choose the codec for both video and audio.
- Option to set the video framerate.
- Option to specify the quality of compression using CRF (Constant Rate Factor).
- Option to set the format container type.
- Option to set the number of threads for FFmpeg.
- Option to set audio filters, such as normalization and equalization.
- Parallel processing of multiple video files for efficiency, with user-defined limit on the number of simultaneous conversions (default max: 5).
- Handles subdirectories, maintaining the original folder structure.
- Supports setting a default or custom bitrate if the original bitrate cannot be determined.
- Generates debug logs for detailed troubleshooting.

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

- **`-b`, `--bitrate`** (optional): Bitrate for the video (e.g., `600k`). If not provided, the original bitrate is used, or a default of `6000k` if the original bitrate cannot be determined.

  Example: `-b 800k`

- **`-r`, `--resolution`** (optional): Resolution for upscaling (e.g., `1280x720`). If not provided, no upscaling is applied.

  Example: `-r 1920x1080`

- **`--preset`** (optional): FFmpeg preset for encoding speed. Choices are `ultrafast`, `superfast`, `veryfast`, `faster`, `fast`, `medium`, `slow`, `slower`, `veryslow`. Defaults to `'slow'` for GPU and `'veryslow'` for CPU if not specified.

  Example: `--preset fast`

- **`--audio_codec`** (optional): Audio codec to use (e.g., `aac`, `mp3`, `opus`). Default is `'aac'`.

  Example: `--audio_codec mp3`

- **`--audio_bitrate`** (optional): Bitrate for the audio (e.g., `128k`). Default is `'128k'`.

  Example: `--audio_bitrate 192k`

- **`--framerate`** (optional): Set the video framerate (e.g., `24`, `30`). If not provided, the original framerate is used.

  Example: `--framerate 30`

- **`--crf`** (optional): Set the quality of compression using CRF (Constant Rate Factor). Lower values mean better quality. Only applies to certain encoders like `libx264` or `libx265`.

  Example: `--crf 23`

- **`--container_format`** (optional): Set the container format (e.g., `mp4`, `mkv`). Default is determined by the output file extension.

  Example: `--container_format mp4`

- **`--threads`** (optional): Set the number of threads for FFmpeg. Default is determined by FFmpeg automatically.

  Example: `--threads 4`

- **`--audio_filter`** (optional): Apply an audio filter (e.g., `volume=1.5` to increase volume by 50%).

  Example: `--audio_filter volume=1.5`

- **`--remove_metadata`** (optional): Remove metadata from the video file.

  Example: `--remove_metadata`

- **`--debug`** (optional): Enable debug mode to generate detailed logs for each conversion.

  Example: `--debug`

- **`--max_simultaneous`** (optional): Set the maximum number of videos to convert simultaneously. Default is `5`.

  Example: `--max_simultaneous 3`

### Examples

1. Convert all video files in a directory to MKV format with the original bitrate:

   ```bash
   python video_converter.py -d /path/to/videos
   ```

2. Convert only `.mp4` and `.avi` files to `.mkv`, upscale to `1280x720`, and remove metadata:

   ```bash
   python video_converter.py -d /path/to/videos -i .mp4 .avi -r 1280x720 --remove_metadata
   ```

3. Convert all video files to `.mp4` format with a custom video bitrate of `800k` and audio bitrate of `192k` using the `mp3` codec:

   ```bash
   python video_converter.py -d /path/to/videos -o .mp4 -b 800k --audio_codec mp3 --audio_bitrate 192k
   ```

4. Convert video files using a faster preset (`veryfast`), set the framerate to `30`, and generate debug logs for troubleshooting:

   ```bash
   python video_converter.py -d /path/to/videos --preset veryfast --framerate 30 --debug
   ```

5. Convert video files, limiting to `3` simultaneous conversions:

   ```bash
   python video_converter.py -d /path/to/videos --max_simultaneous 3
   ```

## How It Works

1. The script detects the type of GPU available (NVIDIA, AMD, or CPU) and selects the appropriate encoder.
2. It collects all the video files that match the input formats specified.
3. It creates an "old" directory in the provided directory to store the original files, preserving the original folder structure.
4. It processes each video using FFmpeg with options like bitrate, resolution, codec, framerate, and metadata removal based on user input.
5. The processing is done in parallel using multiple threads to speed up the conversion of large batches of files, with a user-defined limit on the number of simultaneous conversions.

## Handling Errors

- If FFmpeg is not found in the system's PATH, the script will notify the user.
- If any conversion fails, the original file is restored to its initial location.
- If the original bitrate cannot be determined, a default bitrate of `6000k` is used to ensure the conversion proceeds.

## Notes

- Ensure that FFmpeg is installed and accessible from your command line before running the script. You can install FFmpeg using:
  - **Ubuntu**: `sudo apt-get install ffmpeg`
  - **Windows**: Download from [FFmpeg's official website](https://ffmpeg.org/download.html).

## Contributing

Feel free to submit pull requests or issues to improve this project. Contributions are welcome!

## License

This project is licensed under the GNU General Public License v3.0.

## Acknowledgments

- Thanks to the developers of [FFmpeg](https://ffmpeg.org/) for creating a versatile tool for multimedia processing.
