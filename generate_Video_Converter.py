# Use this script to convert AVI files to MP4 (copies video container & converts audio to AAC codec)
# Tested & works on AVI files

import os
import subprocess

# Directory containing .avi files
directory_path = r'C:\Users\admin\Desktop\Unsorted'

# Loop through all files in the directory
for filename in os.listdir(directory_path):
    if filename.lower().endswith('.avi'):
        input_file = os.path.join(directory_path, filename)
        output_file = os.path.join(directory_path, f"{os.path.splitext(filename)[0]}.MP4")
        
        # ffmpeg command to convert avi to mp4
        command = f'ffmpeg.exe -i "{input_file}" -c:v copy -c:a aac "{output_file}"'
        
        # Run the ffmpeg command using subprocess
        subprocess.run(command, shell=True)
