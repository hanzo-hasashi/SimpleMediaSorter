# This copies specified EXIF tags from files present in Source Directory to the Destination Directory. Files must be present in both the folders with same name...

import os
import subprocess
import json
from config_media_sorter import source_directory_para, destination_directory_para

# # Define the input and output folders
# source_dir = r"D:\Source"
# destination_dir = r"D:\Destination"

# Use Source & Destination from config_media_sorter.py file
source_dir = source_directory_para
destination_dir = destination_directory_para

# Define the list of tags you want to extract and update
tags_to_extract = ["DateTimeOriginal", "CreateDate", "ModifyDate", "TrackCreateDate", "TrackModifyDate", "MediaCreateDate", "MediaModifyDate", "Rotation", "GPSLatitude", "GPSLongitude", "GPSCoordinates", "GPSPosition", "GPSAltitude", "GPSLatitudeRef", "GPSLongitudeRef", "GPSAltitudeRef"]
tags_to_update  = ["DateTimeOriginal", "CreateDate", "ModifyDate", "TrackCreateDate", "TrackModifyDate", "MediaCreateDate", "MediaModifyDate", "Rotation", "GPSLatitude", "GPSLongitude", "GPSCoordinates", "GPSPosition", "GPSAltitude", "GPSLatitudeRef", "GPSLongitudeRef", "GPSAltitudeRef"]

# Iterate through the files in FolderA
for filename in os.listdir(source_dir):
    if filename.endswith(".mp4"):  # Adjust the file extension as needed
        file_path_a = os.path.join(source_dir, filename)
        file_path_b = os.path.join(destination_dir, filename)

        # Extract the specified tags from the image in FolderA
        extract_command = [
            "exiftool",
            "-j",  # Output in JSON format
            *["-" + tag for tag in tags_to_extract],
            file_path_a,
        ]

        extract_result = subprocess.run(
            extract_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        if extract_result.returncode == 0:
            try:
                extracted_metadata = json.loads(extract_result.stdout)[0]

                # Create the update command for the image in FolderB
                update_command = [
                    "exiftool",
                    *["-" + tag + "=" + str(extracted_metadata.get(tag, "")) for tag in tags_to_update],
                    file_path_b,
                ]

                # Run the update command for the image in FolderB
                update_result = subprocess.run(
                    update_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )

                if update_result.returncode == 0:
                    print(f"Updated tags in {filename}")
                else:
                    print(f"Error updating tags in {filename}: {update_result.stderr}")

            except json.JSONDecodeError:
                print(f"Error parsing JSON output for {filename}")

        else:
            print(f"Error extracting tags from {filename}: {extract_result.stderr}")
