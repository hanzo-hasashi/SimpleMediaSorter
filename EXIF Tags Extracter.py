import os
import subprocess
import csv
from datetime import datetime

source_dir = r"C:\Users\admin\Desktop\Unsorted"  # Change this to the path of your folder
output_csv = os.path.join(source_dir, "video_details.csv") # This file stores the EXIF info extracted from files 

def get_video_details(file_path):
    try:
        exiftool_output = subprocess.check_output(["exiftool", "-Encoder", "-HandlerDescription", "-FileSize", "-MediaCreateDate", file_path], universal_newlines=True)
        exiftool_lines = exiftool_output.strip().split('\n')
        
        video_details = {}
        
        for line in exiftool_lines:
            parts = line.split(": ", 1)
            if len(parts) == 2:
                key, value = parts
                video_details[key.strip()] = value.strip()
        
        return video_details
    except subprocess.CalledProcessError as e:
        return None

def find_and_save_video_details(folder_path, output_csv):
    allowed_extensions = {".mp4", ".mov", ".3gp", ".avi"}
    
    with open(output_csv, mode='w', newline='') as csv_file:
        fieldnames = ['Filename', 'FileLocation', 'FileSize', 'MediaCreateDate', 'Encoder', 'HandlerDescription']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_extension = os.path.splitext(file)[-1].lower()
                if file_extension in allowed_extensions:
                    file_path = os.path.join(root, file)
                    video_details = get_video_details(file_path)
                    if video_details:
                        filename = os.path.basename(file_path)
                        file_location = file_path
                        file_size = video_details.get("File Size", "N/A")
                        media_create_date = video_details.get("Media Create Date", "N/A")
                        encoder = video_details.get("Encoder", "N/A")
                        handler_description = video_details.get("Handler Description", "N/A")

                        writer.writerow({
                            'Filename': filename,
                            'FileLocation': file_location,
                            'FileSize': file_size,
                            'MediaCreateDate': media_create_date,
                            'Encoder': encoder,
                            'HandlerDescription': handler_description
                        })

                        print(f"Processed: {file_path}")

if __name__ == "__main__":
    find_and_save_video_details(source_dir, output_csv)
    print(f"Video details have been saved to {output_csv}")