# Copies files with specific extension while maintaining the folder structure

import os
import shutil
from config_media_sorter import source_directory_para, destination_directory_para

# Use Source & Destination from config_media_sorter.py file
source_dir = source_directory_para
destination_dir = destination_directory_para

# Ensure the destination directory exists
if not os.path.exists(source_dir):
    os.makedirs(destination_dir)

# Function to copy .jpg and .nef files while maintaining folder structure
def copy_images(src, dst):
    for root, _, files in os.walk(src):
        for file in files:
            if file.endswith(('.MOV', '.nef')):
                source_file = os.path.join(root, file)
                relative_path = os.path.relpath(source_file, src)
                destination_file = os.path.join(dst, relative_path)
                
                # Ensure the destination directory exists
                destination_folder = os.path.dirname(destination_file)
                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                
                # Copy the file to the destination directory
                shutil.copy(source_file, destination_file)
                print(f'Copied: {source_file} to {destination_file}')

# Copy the images
copy_images(source_dir, destination_dir)
