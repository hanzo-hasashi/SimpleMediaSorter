import os
import subprocess

source_dir = r"C:\Users\admin\Desktop\Unsorted"  # Change this to the path of your folder
keyword = "Google"  # Change this to your desired keyword

def get_handler_description(file_path):
    try:
        exiftool_output = subprocess.check_output(["exiftool", "-HandlerDescription", file_path], universal_newlines=True)
        return exiftool_output.strip()
    except subprocess.CalledProcessError as e:
        return None

def find_processed_by_keyword(folder_path, keyword, allowed_extensions):
    matching_files = []

    for root, _, files in os.walk(folder_path):
        for file in files:
            file_extension = os.path.splitext(file)[-1].lower()
            if file_extension in allowed_extensions:
                file_path = os.path.join(root, file)
                handler_description = get_handler_description(file_path)
                if handler_description and keyword in handler_description:
                    matching_files.append(file_path)

    return matching_files

if __name__ == "__main__":
    allowed_extensions = {".mp4", ".mov", ".3gp", ".avi"}
    matching_files = find_processed_by_keyword(source_dir, keyword, allowed_extensions)

    if matching_files:
        print("Files with keyword '{}' in HandlerDescription:".format(keyword))
        for file_path in matching_files:
            print(file_path)
    else:
        print("No files found with keyword '{}' in HandlerDescription.".format(keyword))
