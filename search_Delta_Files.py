# Use this script to search delta files (unique ones) in folder A when compared with folder B. It also copies unique files in Destination folder
# Tested, works on all types of files

import os
import shutil

# Define your source and destination folders
folder_a_path = r'C:\Users\admin\Downloads\Takeout\Google Photos'  # Replace 'Folder A' with the path to your Folder A
folder_b_path = r'E:\Media\PhotoSpace'  # Replace 'Folder B' with the path to your Folder B
destination_path = r'C:\Users\admin\Downloads\UniqueFiles'  # Replace 'Destination Folder' with your desired destination path

def compare_and_copy(source_folder_a, source_folder_b, destination_folder):
    # Dictionary to store filenames and their absolute paths from Folder A
    file_dict = {}
    
    # Traverse Folder A and store filenames and their absolute paths in the dictionary
    for foldername, _, filenames in os.walk(source_folder_a):
        for filename in filenames:
            file_dict[filename] = os.path.join(foldername, filename)

    # Traverse Folder B and remove filenames found in both folders from the dictionary
    for foldername, _, filenames in os.walk(source_folder_b):
        for filename in filenames:
            file_dict.pop(filename, None)

    # Create the Destination Folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Copy unique files from Folder A to the Destination Folder while maintaining the folder structure
    for filename, abs_path in file_dict.items():
        relative_path = os.path.relpath(abs_path, source_folder_a)
        destination_path = os.path.join(destination_folder, relative_path)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)
        shutil.copy2(abs_path, destination_path)
        print(f"File '{filename}' copied to Destination Folder")

# Call the function
compare_and_copy(folder_a_path, folder_b_path, destination_path)
