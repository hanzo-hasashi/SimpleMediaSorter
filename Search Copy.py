# Searches and copies files while retaining the folder structure...

import os
import shutil
from config_media_sorter import source_directory_para, destination_directory_para

# Use Source & Destination from config_media_sorter.py file
source_dir = source_directory_para
destination_dir = destination_directory_para

# List of files to search for and copy
file_list = [".mov"]

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Function to search and copy files
def copy_files(source, destination, files_to_copy):
    for root, _, files in os.walk(source):
        for file in files:
            if file in files_to_copy:
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination, file)

                # Copy the file to the destination
                shutil.copy2(source_path, destination_path)
                print(f"Copying {file} to {destination_path}")

# Call the function to search and copy the specified files
copy_files(source_dir, destination_dir, file_list)
