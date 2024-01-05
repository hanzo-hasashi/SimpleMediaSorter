# Use this script to generate thumbnail on video files using ffmpeg
# Tested, works on MOV & MP4 files

import subprocess
import os
import shutil

# Set the Working Directory
directory_path = r'C:\Users\admin\Desktop\Unsorted'

def extract_thumbnail(video_path, output_thumbnail):
    # Get video duration using FFmpeg
    duration_command = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {video_path}'
    duration_process = subprocess.Popen(duration_command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    duration_output, _ = duration_process.communicate()

    duration = float(duration_output)
    thumbnail_time = 5 if duration > 5 else 1  # Set thumbnail time

    # Extract thumbnail using FFmpeg
    thumbnail_command = f'ffmpeg -i {video_path} -ss {thumbnail_time} -vframes 1 {output_thumbnail}'
    subprocess.run(thumbnail_command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return thumbnail_time

def embed_thumbnail(video_path, thumbnail_path, output_path):
    # Embed thumbnail into video using FFmpeg, preserving metadata and EXIF tags
    embed_command = f'ffmpeg -i {video_path} -i {thumbnail_path} -map 0 -map 1 -c copy -map_metadata 0 -disposition:v:1 attached_pic {output_path}'
    subprocess.run(embed_command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def process_video_directory(directory):
    successfully_updated_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Check if file is a video
                video_file = os.path.join(root, file)
                output_thumbnail = os.path.join(root, f'{os.path.splitext(file)[0]}_thumbnail.jpg')
                destination_folder = os.path.join(directory, "Processed")
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)

                thumbnail_time = extract_thumbnail(video_file, output_thumbnail)

                if os.path.exists(output_thumbnail):
                    output_video = os.path.join(destination_folder, file)
                    embed_thumbnail(video_file, output_thumbnail, output_video)
                    print(f"Thumbnail extracted at {thumbnail_time} second(s) from {file} and embedded into the video.")
                    os.remove(output_thumbnail)

                    successfully_updated_files.append(file)
                else:
                    print(f"Thumbnail extraction failed for {file}.")

    return successfully_updated_files

if __name__ == "__main__":
    video_directory = directory_path  # Replace with your video directory
    updated_files = process_video_directory(video_directory)