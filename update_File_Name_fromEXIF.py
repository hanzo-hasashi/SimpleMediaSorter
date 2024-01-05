# Use this script to update filename.jpg to filename_Date_Time.jpg
# Tested, works on Image & Video files

import os
import exifread
from datetime import datetime
import subprocess
import shutil

# Set the Working Directory
directory_path = r'C:\Users\admin\Desktop\Unsorted\More'

def get_img_creation_date(file_path):
    with open(file_path, 'rb') as image_file:
        tags = exifread.process_file(image_file)
        if 'EXIF DateTimeOriginal' in tags:
            date_obj = tags['EXIF DateTimeOriginal'].printable
            creation_date_sanitized = datetime.strptime(date_obj, "%Y:%m:%d %H:%M:%S").strftime('%Y%m%d_%H%M%S')
            return creation_date_sanitized
    return None

def get_vid_creation_date(file_path):
    # Attempt to retrieve creation date using MediaCreateDate tag
    result = subprocess.run(
        ["exiftool", "-s", "-s", "-s", "-MediaCreateDate", file_path],
        capture_output=True,
        text=True,
        check=True
    )
    media_create_date = result.stdout.strip()
    # If MediaCreateDate returns a placeholder value, try CreateDate
    if media_create_date == '0000:00:00 00:00:00':
        result = subprocess.run(
            ["exiftool", "-s", "-s", "-s", "-CreateDate", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        media_create_date = result.stdout.strip()
    creation_date_sanitized = datetime.strptime(media_create_date, "%Y:%m:%d %H:%M:%S").strftime('%Y%m%d_%H%M%S')
    return creation_date_sanitized


def rename_files_with_date(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename.lower().endswith(('.jpg', '.jpeg', '.nef', '.gif')):
            creation_date = get_img_creation_date(file_path)
            if creation_date:
                old_filename = f"{os.path.splitext(filename)[0]}"
                extension = os.path.splitext(filename)[1]  # Get the original file extension
                new_filename = f"{old_filename}_{creation_date}{extension}"
                os.rename(file_path, os.path.join(directory, new_filename))
                print('Renamed IMG:', filename,'to', new_filename)
        elif file_path.lower().endswith(('.mov', '.mp4', '.mkv', '.3gp')):            
            creation_date = get_vid_creation_date(file_path)
            if creation_date:
                old_filename = f"{os.path.splitext(filename)[0]}"
                extension = os.path.splitext(filename)[1]  # Get the original file extension
                new_filename = f"{old_filename}_{creation_date}{extension}"
                os.rename(file_path, os.path.join(directory, new_filename))
                print('Renamed VID:', filename,'to', new_filename)
            
rename_files_with_date(directory_path)
