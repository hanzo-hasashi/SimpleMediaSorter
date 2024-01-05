# Use this script to extract DateTime from file (YYYYMMDD) and update it in the EXIF
# Tested, works on Image (EXIF tag) & Video (QuickTime tag) files

import os
import re
import subprocess

# Set the Working Directory
directory_path = r'D:\Data\Pictures\AlbumRestoration\Renamed\JPG'

def extract_date_from_filename(filename):
    match = re.search(r'(\d{4})(\d{2})(\d{2})(?:_(\d{2})(\d{2})(\d{2}))?', filename)
    if match:
        groups = match.groups()
        if groups[3] is not None:  # If time info is present
            year, month, day, hour, minute, second = map(int, groups[:6])
        else:  # If only date info is present
            year, month, day = map(int, groups[:3])
            hour, minute, second = 12, 0, 0  # Assign default time 12:00:00
        return f"{year}:{month:02}:{day:02} {hour:02}:{minute:02}:{second:02}"
    return None

def update_exif_date_time(image_file, new_date_time, file_extension):
    try:
        if file_extension.lower() in ['.jpg', '.jpeg']:
            subprocess.run(['exiftool', '-DateTimeOriginal=' + new_date_time, '-CreateDate=' + new_date_time, image_file], check=True)
            print(f"Updated EXIF data for {image_file}")
        elif file_extension.lower() == '.gif':
            subprocess.run(['exiftool', '-FileCreateDate=' + new_date_time, image_file], check=True)
            print(f"Updated FileCreateDate for {image_file}")
        else:
            print(f"Unsupported file type for {image_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error updating metadata for {image_file}: {e}")

def update_exif_quicktime_tags(video_file, new_date_time):
    try:
        subprocess.run([
            'exiftool',
            f'-CreateDate={new_date_time}',
            f'-ModifyDate={new_date_time}',
            f'-TrackCreateDate={new_date_time}',
            f'-TrackModifyDate={new_date_time}',
            f'-MediaCreateDate={new_date_time}',
            f'-MediaModifyDate={new_date_time}',
            '-overwrite_original',  # Overwrite original file (without creating backup)
            '-P',  # Preserve file modification date/time
            '-q',  # Quiet mode
            video_file
        ], check=True)
        print(f"Updated EXIF QuickTime tags for {video_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error updating EXIF QuickTime tags for {video_file}: {e}")

def update_file_datetime(file_path, new_date_time):
    try:
        # Update file's creation time and modification time
        os.utime(file_path, (os.stat(file_path).st_atime, new_date_time))
        print(f"Updated datetime for {file_path}")
    except Exception as e:
        print(f"Error updating datetime for {file_path}: {e}")

# Process IMG & VID files
for filename in os.listdir(directory_path):
    file_extension = os.path.splitext(filename)[1]
    full_path = os.path.join(directory_path, filename)
    
    if file_extension.lower() in ['.jpg', '.jpeg', '.nef', '.gif']:
        extracted_date = extract_date_from_filename(filename)
        if extracted_date:
            update_exif_date_time(full_path, extracted_date, file_extension)
        else:
            print(f"Couldn't extract date from PHOTO filename: {filename}")
    elif file_extension.lower() in ['.mov', '.mp4', '.mkv', '.3gp']:  
        full_path = os.path.join(directory_path, filename)
        extracted_date = extract_date_from_filename(filename)
        if extracted_date:
            update_exif_quicktime_tags(full_path, extracted_date)
        else:
            print(f"Couldn't extract date from VIDEO filename: {filename}")

    else:
        print(f"Unkown filetype: {filename}")
