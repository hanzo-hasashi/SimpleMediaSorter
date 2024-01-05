import subprocess
import os

def update_exif_with_exiftool(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.jpg'):
                file_path = os.path.join(root, file)
                try:
                    # Extract file modification date
                    modify_date = subprocess.check_output(['exiftool', '-FileModifyDate', '-s', '-s', '-s', file_path]).decode('utf-8').strip()

                    # Update DateTimeOriginal tag using ExifTool
                    # subprocess.run(['exiftool', '-DateTimeOriginal=' + modify_date, file_path])
                    subprocess.run([
                    'exiftool',
                    f'-CreateDate={modify_date}',
                    f'-DateTimeOriginal={modify_date}',
                    f'-TrackCreateDate={modify_date}',
                    f'-TrackModifyDate={modify_date}',
                    f'-MediaCreateDate={modify_date}',
                    f'-MediaModifyDate={modify_date}',
                    '-overwrite_original',  # Overwrite original file (without creating backup)
                    '-P',  # Preserve file modification date/time
                    '-q',  # Quiet mode
                    file_path
                    ], check=True)
                 
                    print(f"Updated DateTimeOriginal for {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")

# Replace 'folder_path' with the path to your folder containing JPG files
folder_path = r'C:\Users\admin\Desktop\Unsorted'
update_exif_with_exiftool(folder_path)
