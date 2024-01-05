import os
import csv
from datetime import datetime
import exifread
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

def extract_capture_date_image(file_path):
    try:
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.nef', '.dng', '.gif', '.tif')):
            with open(file_path, 'rb') as file:
                tags = exifread.process_file(file)
                date_taken = tags.get('EXIF DateTimeOriginal')
                if date_taken:
                    return datetime.strptime(str(date_taken), '%Y:%m:%d %H:%M:%S')
        return None
    except Exception as e:
        # Log or handle the specific exception here if required
        pass

def extract_capture_date_video(file_path):
    try:
        if file_path.lower().endswith(('.mov', '.mp4', '.mkv', '.3gp', '.avi', '.m4v', '.mpg')):
            parser = createParser(file_path)
            if parser:
                metadata = extractMetadata(parser)
                if metadata:
                    return metadata.get('creation_date')
        return None
    except Exception as e:
        # Log or handle the specific exception here if required
        pass

def write_row_to_csv(csv_writer, file_path, capture_date):
    file_name = os.path.basename(file_path)
    if isinstance(capture_date, datetime):
        date_str = capture_date.strftime('%d-%m-%Y')
        time_str = capture_date.strftime('%I:%M %p')  # HH:MM AM/PM format
    else:
        date_str = ''
        time_str = ''

    csv_writer.writerow([file_path, file_name, date_str, time_str])

def generate_csv(source_folder, output_csv):
    supported_extensions = (
        '.jpg', '.jpeg', '.png', '.nef', '.dng', '.gif', '.tif',
        '.mov', '.mp4', '.mkv', '.3gp', '.avi', '.m4v', '.mpg'
    )

    file_list = []
    unsupported_files = []

    for root, _, files in os.walk(source_folder):
        for file in files:
            file_path = os.path.join(root, file)
            file_list.append(file_path)

    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Full File Name', 'File Name', 'Date', 'Time'])

        for file_path in file_list:
            print("Processing:", file_path)

            capture_date = None

            if file_path.lower().endswith(supported_extensions):
                capture_date = extract_capture_date_image(file_path) or extract_capture_date_video(file_path)
            else:
                unsupported_files.append(file_path)

            if capture_date is not None:
                write_row_to_csv(csv_writer, file_path, capture_date)
            else:
                csv_writer.writerow([file_path, os.path.basename(file_path), '', ''])

        if unsupported_files:
            print("Unsupported Files:")
            for file_path in unsupported_files:
                print(file_path)

if __name__ == "__main__":
    source_folder = r'E:\Media\PhotoSpace'
    output_csv = 'PhotoSpace_Output.csv'
    generate_csv(source_folder, output_csv)
