# Copies specific files while maintaining the folder structure

import os
import shutil
from config_media_sorter import source_directory_para, destination_directory_para

# # Define the input and output folders
# source_dir = r"D:\Source"
# destination_dir = r"D:\Destination"

# Use Source & Destination from config_media_sorter.py file
source_dir = source_directory_para
destination_dir = destination_directory_para

# Create the destination directory if it doesn't exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Ask the user whether to copy or move files
action = input("Do you want to copy or move the files? (copy/move): ").strip().lower()

if action not in ["copy", "move"]:
    print("Invalid choice. Please enter 'copy' or 'move'.")
else:
    # Define a function to copy or move files while retaining the folder structure
    def process_files(source, destination, action):
        for root, _, files in os.walk(source):
            for file in files:
                file_path = os.path.join(root, file)
                if file.lower().endswith((".mp4",".mov", ".avi", ".3gp", ".m4v", ".mpg")):
                    relative_path = os.path.relpath(file_path, source)
                    destination_path = os.path.join(destination, relative_path)
                    destination_folder = os.path.dirname(destination_path)

                    # Create the destination folder if it doesn't exist
                    if not os.path.exists(destination_folder):
                        os.makedirs(destination_folder)

                    if action == "copy":
                        # Copy the file to the destinationcop
                        shutil.copy2(file_path, destination_path)
                        print(f"Copying {file} to {destination_path}")
                    elif action == "move":
                        # Move the file to the destination
                        shutil.move(file_path, destination_path)
                        print(f"Moving {file} to {destination_path}")

    # Call the function to copy or move
    process_files(source_dir, destination_dir, action)
