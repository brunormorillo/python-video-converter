import os
import subprocess
import argparse
import sys
from tqdm import tqdm  # Library for displaying progress bars in the terminal
import time  # Used to simulate a delay in execution for testing

# Function to detect the type of GPU (NVIDIA, AMD, or CPU)
def detect_gpu():
    try:
        # Check if an NVIDIA GPU is available
        nvidia_info = subprocess.check_output(["nvidia-smi", "-L"]).decode("utf-8")
        if "GPU" in nvidia_info:
            return "nvidia"
    except Exception:
        pass

    try:
        # Check if an AMD GPU is available using WMIC command on Windows
        amd_info = subprocess.check_output(
            ["wmic", "path", "win32_VideoController", "get", "name"]
        ).decode("utf-8")
        if "AMD" in amd_info or "Radeon" in amd_info:
            return "amd"
    except Exception:
        pass

    # If no GPU is detected, default to "cpu"
    return "cpu"

# Function to check if ffmpeg is installed and get its version
def check_ffmpeg():
    try:
        # Run the ffmpeg command to get its version
        ffmpeg_version_info = subprocess.check_output(
            ["ffmpeg", "-version"], stderr=subprocess.STDOUT
        ).decode("utf-8")
        for line in ffmpeg_version_info.split("\n"):
            if "ffmpeg version" in line:
                return line  # Return ffmpeg version information
    except FileNotFoundError:
        return "FFmpeg not found in PATH"  # Error message if ffmpeg is not found
    return "FFmpeg not found"

# Function to get the original bitrate of a video file
def get_original_bitrate(video_file):
    try:
        # Use ffprobe to retrieve the video's bitrate
        result = subprocess.check_output(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=bit_rate", "-of", "default=noprint_wrappers=1:nokey=1", video_file]
        ).decode("utf-8").strip()
        return f"{int(result) // 1000}k"  # Convert to kbps and return as a string
    except Exception as e:
        print(f"Error getting original bitrate: {e}")
        return None

# Set up command-line arguments
parser = argparse.ArgumentParser(
    description="Convert video files to a specific format with optional upscaling and metadata removal."
)
parser.add_argument(
    "-d",
    "--directory",
    type=str,
    required=True,
    help="Directory where the videos are located.",
)
parser.add_argument(
    "-i",
    "--input_formats",
    nargs="*",
    default=None,
    help="Input formats of the files to be converted (e.g., .mp4 .ts). If none are provided, all video files will be converted.",
)
parser.add_argument(
    "-o",
    "--output_format",
    type=str,
    default=".mkv",
    help="Output format of the converted files (default: .mkv).",
)
parser.add_argument(
    "-b",
    "--bitrate",
    type=str,
    default=None,
    help="Bitrate for the video (e.g., 600k). If not provided, the original bitrate is used.",
)
parser.add_argument(
    "-r",
    "--resolution",
    type=str,
    default=None,
    help="Resolution for upscaling (e.g., 1280x720). If not provided, no upscaling is applied.",
)
parser.add_argument(
    "--remove_metadata",
    action="store_true",
    help="Remove metadata from the video file.",
)
args = parser.parse_args()

# Display ffmpeg version
ffmpeg_version = check_ffmpeg()
print(ffmpeg_version)

# Set the directory where videos are located
directory = args.directory

# Collect all video files to be converted
files_to_convert = []
for root, dirs, files in os.walk(directory):
    for file in files:
        # Check if the file matches the specified input formats
        if args.input_formats is None or file.endswith(tuple(args.input_formats)):
            files_to_convert.append(os.path.join(root, file))

# Count the total number of files for conversion and display this info
total_files = len(files_to_convert)
print(f"Starting conversion of {total_files} files...")

# Detect the type of available GPU
gpu_type = detect_gpu()
print(f"Using {gpu_type.upper()} for processing.")

# Set the video encoder based on GPU type
if gpu_type == "nvidia":
    video_encoder = "hevc_nvenc"
    preset = "slow"
elif gpu_type == "amd":
    video_encoder = "hevc_amf"
    preset = "slow"
else:
    video_encoder = "libx265"
    preset = "veryslow"

if total_files > 0:
    # Create an 'old' folder to store the original files
    old_directory = os.path.join(directory, "old")
    if not os.path.exists(old_directory):
        os.mkdir(old_directory)

    # Overall progress bar for all files
    with tqdm(total=total_files, desc="Total Progress", unit="file") as pbar_total:
        for idx, file in enumerate(files_to_convert, start=1):
            full_name = file
            old_full_name = os.path.join(old_directory, os.path.basename(full_name))
            output_name = os.path.splitext(full_name)[0] + args.output_format

            # Move the original file to the .old folder before processing
            os.rename(full_name, old_full_name)

            print(f"Processing file {idx}/{total_files}: {os.path.basename(old_full_name)}")

            # Determine the video's bitrate
            video_bitrate = args.bitrate if args.bitrate else get_original_bitrate(old_full_name)

            # Build the ffmpeg command for video conversion
            command = [
                "ffmpeg",
                "-i",
                old_full_name,  # Now points to the file in the .old folder
                "-c:v",
                video_encoder,
                "-b:v",
                video_bitrate,
                "-preset",
                preset,
                "-c:a",
                "aac",
                "-b:a",
                "128k",
                "-progress", "-",  # Adds detailed progress output
            ]

            # Add upscaling if a resolution is specified
            if args.resolution:
                command.extend(["-vf", f"scale={args.resolution}"])

            # Remove metadata if the option is enabled
            if args.remove_metadata:
                command.extend(["-map_metadata", "-1"])

            command.append(output_name)
            print(f"Executing command: {' '.join(command)}")

            # Execute the ffmpeg command with detailed output
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
            )

            # Progress bar for the individual file
            with tqdm(total=100, desc=f"{os.path.basename(old_full_name)} Progress", leave=False) as pbar_file:
                for line in process.stdout:
                    # Simulate progress bar update based on time (adjust as needed)
                    if "frame=" in line or "time=" in line:
                        if "time=" in line:
                            pbar_file.update(1)  # Adjust progress metric here
                    time.sleep(0.1)  # Remove for real execution; just for simulation

                process.wait()
                print(f"Finished processing file: {os.path.basename(old_full_name)}")

            pbar_total.update(1)  # Update the overall progress bar after each file is complete

        print("Conversion completed!")
else:
    print("No files to convert found.")
