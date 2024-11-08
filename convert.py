import os
import subprocess
import argparse
import sys
from tqdm import tqdm
import re  # Library for parsing FFmpeg output
from concurrent.futures import ThreadPoolExecutor

# Function to detect the type of GPU (NVIDIA, AMD, or CPU)
def detect_gpu():
    try:
        nvidia_info = subprocess.check_output(["nvidia-smi", "-L"]).decode("utf-8")
        if "GPU" in nvidia_info:
            return "nvidia"
    except Exception:
        pass

    try:
        amd_info = subprocess.check_output(["lspci"], stderr=subprocess.DEVNULL).decode("utf-8")
        if "AMD" in amd_info or "Radeon" in amd_info:
            return "amd"
    except Exception:
        pass

    return "cpu"

# Function to check if ffmpeg is installed and get its version
def check_ffmpeg():
    try:
        ffmpeg_version_info = subprocess.check_output(
            ["ffmpeg", "-version"], stderr=subprocess.STDOUT
        ).decode("utf-8")
        for line in ffmpeg_version_info.split("\n"):
            if "ffmpeg version" in line:
                return line
    except FileNotFoundError:
        return "FFmpeg not found in PATH"
    return "FFmpeg not found"

# Function to get the original bitrate of a video file
def get_original_bitrate(video_file):
    try:
        result = subprocess.check_output(
            [
                "ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=bit_rate",
                "-of", "default=noprint_wrappers=1:nokey=1", video_file
            ]
        ).decode("utf-8").strip()
        return f"{int(result) // 1000}k"
    except Exception as e:
        print(f"Error getting original bitrate: {e}")
        return None

# Function to process each video file
def process_video(file, args, gpu_type, video_encoder, preset, old_directory):
    try:
        old_full_name = os.path.join(old_directory, os.path.basename(file))
        output_name = os.path.splitext(file)[0] + args.output_format

        print(f"Processing file: {os.path.basename(old_full_name)}")

        video_bitrate = args.bitrate if args.bitrate else get_original_bitrate(old_full_name)

        command = [
            "ffmpeg",
            "-i",
            old_full_name,
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
            "-progress", "pipe:1"
        ]

        if args.resolution:
            command.extend(["-vf", f"scale={args.resolution}"])

        if args.remove_metadata:
            command.extend(["-map_metadata", "-1"])

        command.append(output_name)
        print(f"Executing command: {' '.join(command)}")

        log_file_path = os.path.splitext(output_name)[0] + "_conversion.log"
        if args.debug:
            log_file = open(log_file_path, "w")
        else:
            log_file = open(os.devnull, "w")

            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )

            with tqdm(total=100, desc=f"{os.path.basename(old_full_name)} Progress", leave=False) as pbar_file:
                progress = 0
                for line in process.stdout:
                    if args.debug:
                        log_file.write(line)  # Write each line to the log file if debug is enabled
                    match = re.search(r"out_time_ms=(\d+)", line)
                    if match:
                        progress = min(100, int(match.group(1)) // 1000000)  # Convert to seconds
                        pbar_file.n = progress
                        pbar_file.refresh()

                process.wait()
                log_file.close()

                if process.returncode != 0:
                    raise subprocess.CalledProcessError(process.returncode, command)
                # Ensure the bar is completed after process ends
                pbar_file.n = 100
                pbar_file.refresh()
                pbar_file.close()
                print(f"Finished processing file: {os.path.basename(old_full_name)}")

    except subprocess.CalledProcessError as e:
        print(f"Error processing file {os.path.basename(file)}: {e}")
        # Delete the output file if it exists and restore the original file
        if os.path.exists(output_name):
            os.remove(output_name)
        os.rename(old_full_name, file)

# Set up command-line arguments
parser = argparse.ArgumentParser(
    description="Convert video files to a specific format with optional upscaling and metadata removal."
)
parser.add_argument("-d", "--directory", type=str, required=True, help="Directory where the videos are located.")
parser.add_argument("-i", "--input_formats", nargs="*", default=None, help="Input formats of the files to be converted (e.g., .mp4 .ts). If none are provided, all video files will be converted.")
parser.add_argument("-o", "--output_format", type=str, default=".mkv", help="Output format of the converted files (default: .mkv).")
parser.add_argument("-b", "--bitrate", type=str, default=None, help="Bitrate for the video (e.g., 600k). If not provided, the original bitrate is used.")
parser.add_argument("-r", "--resolution", type=str, default=None, help="Resolution for upscaling (e.g., 1280x720). If not provided, no upscaling is applied.")
parser.add_argument("--remove_metadata", action="store_true", help="Remove metadata from the video file.")
parser.add_argument("--debug", action="store_true", help="Enable debug mode to generate detailed logs for each conversion.")
args = parser.parse_args()

# Display ffmpeg version
ffmpeg_version = check_ffmpeg()
print(ffmpeg_version)

directory = args.directory

# Collect all video files to be converted
files_to_convert = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if args.input_formats is None or file.endswith(tuple(args.input_formats)):
            files_to_convert.append(os.path.join(root, file))

total_files = len(files_to_convert)
print(f"Starting conversion of {total_files} files...")

gpu_type = detect_gpu()
print(f"Using {gpu_type.upper()} for processing.")

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
    old_directory = os.path.join(directory, "old")
    if not os.path.exists(old_directory):
        os.mkdir(old_directory)

    # Move all files to the "old" directory before starting conversion
    for file in files_to_convert:
        old_full_name = os.path.join(old_directory, os.path.basename(file))
        os.rename(file, old_full_name)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(process_video, file, args, gpu_type, video_encoder, preset, old_directory) for file in files_to_convert]
        for future in tqdm(futures, desc="Total Progress", unit="file"):
            future.result()

    print("Conversion completed!")
else:
    print("No files to convert found.")
