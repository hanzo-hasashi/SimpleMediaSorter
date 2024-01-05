# This search for EXIF Tag "keyword" and moves them to a sub-folder

import os
import subprocess
import shutil

source_dir = r"C:\Users\admin\Videos\Handbrake\2015" # Change this to the path of your folder

def get_handler_description(file_path):
    try:
        exiftool_output = subprocess.check_output(["exiftool", "-HandlerDescription", file_path], universal_newlines=True)
        return exiftool_output.strip()
    except subprocess.CalledProcessError as e:
        return None

def find_processed_by_keyword(folder_path, keyword):
    matching_files = []
    
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            handler_description = get_handler_description(file_path)
            if handler_description and keyword in handler_description:
                matching_files.append(file_path)
    
    return matching_files

def move_files_to_subfolders(files, keyword):
    for file_path in files:
        # Create a subfolder named after the keyword
        subfolder = os.path.join(os.path.dirname(file_path), keyword)
        
        # Create the subfolder if it doesn't exist
        if not os.path.exists(subfolder):
            os.makedirs(subfolder)
        
        # Move the file into the subfolder
        shutil.move(file_path, os.path.join(subfolder, os.path.basename(file_path)))

if __name__ == "__main__":
    folder_path = source_dir  # Change this to the path of your folder
    keyword = "Google"  # Change this to your desired keyword

    matching_files = find_processed_by_keyword(folder_path, keyword)

    if matching_files:
        print("Files with keyword '{}' in HandlerDescription:".format(keyword))
        for file_path in matching_files:
            print(file_path)

        move_files_to_subfolders(matching_files, keyword)
        print("Files moved to subfolders with the keyword '{}'.".format(keyword))
    else:
        print("No files found with keyword '{}' in HandlerDescription.".format(keyword))