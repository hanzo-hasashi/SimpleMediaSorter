# Use this script to move video files to "YYYY\MMYY" folder (example 2019\0119 January) this date is extracted from QuickTime tag
# Tested, works on Image (EXIF tag) & Video (QuickTime tag) files

import os
import exifread
from datetime import datetime
import subprocess
import shutil

# Set the Working Directory
directory_path = r'C:\Users\admin\Desktop\Unsorted'

def extract_capture_date(file_path):
    try:
        # Check file extension to determine whether it's an image or video
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.nef')): # Image formats
            with open(file_path, 'rb') as file:
                tags = exifread.process_file(file)
                date_taken = tags.get('EXIF DateTimeOriginal')
                if date_taken:
                    return date_taken
                    # return datetime.strptime(str(date_taken), '%Y:%m:%d %H:%M:%S').strftime('%m%y %B') # returns date in MMYY MMMM format (0101 January)

        elif file_path.lower().endswith(('.mov', '.mp4', '.mkv', '.3gp', '.m4v')):  # Video formats
            result = subprocess.run(
                ["exiftool", "-s", "-s", "-s", "-MediaCreateDate", file_path],
                capture_output=True,
                text=True,
                check=True)
            media_create_date = result.stdout.strip()
            # If MediaCreateDate returns a placeholder value, try CreateDate
            if media_create_date == '0000:00:00 00:00:00':
                result = subprocess.run(
                    ["exiftool", "-s", "-s", "-s", "-CreateDate", file_path],
                    capture_output=True,
                    text=True,
                    check=True)
                media_create_date = result.stdout.strip()
            return media_create_date

        return None
    except Exception as e:
        pass

def organize_files(source_folder):
    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            extension = os.path.splitext(file)[1][1:].upper()  # Get the original file extension
            capture_date = extract_capture_date(file_path)
            if capture_date:
                date_obj = datetime.strptime(str(capture_date), '%Y:%m:%d %H:%M:%S')
                year = date_obj.strftime("%Y")
                month_year = date_obj.strftime("%m%y")
                month_name = date_obj.strftime("%B")
                destination_folder = os.path.join(source_folder, f"{year}/{month_year} {month_name}") # This defines the folder pattern YYYY\MMYY MMMM
                # destination_folder = os.path.join(source_folder, f"{year}") # This defines the folder pattern YYYY
                os.makedirs(destination_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(destination_folder, file))
                print(f"{extension} file moved {file} to {destination_folder}")

if __name__ == "__main__":
    organize_files(directory_path)