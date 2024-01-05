import os
import csv
import subprocess

def get_exif_data(folder_path):
    # List all files in the given folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Set to store all unique field names
    all_fieldnames = set()
    # List to store filepaths
    file_paths = []

    # Open CSV file for writing
    with open('exif_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=[], extrasaction='ignore')

        # Iterate through each file in the folder
        for file in files:
            file_path = os.path.join(folder_path, file)
            file_paths.append(file_path)  # Store the filepath

            # Run exiftool command
            exif_output = subprocess.run(['exiftool', '-time:all', file_path], capture_output=True, text=True)

            # Get the output and split into lines
            exif_lines = exif_output.stdout.splitlines()

            # Parse and extract the relevant data
            exif_data = {'Filepath': file_path, 'Filename': file}
            for line in exif_lines:
                if ':' in line:
                    key, value = map(str.strip, line.split(':', 1))
                    exif_data[key] = value
                    all_fieldnames.add(key)  # Add field name to the set

            # Write header row with all dynamic field names
            if not csv_writer.fieldnames:
                fieldnames = ['Filepath', 'Filename'] + list(all_fieldnames)
                csv_writer.fieldnames = fieldnames
                csv_writer.writeheader()

            # Write data to CSV file
            csv_writer.writerow(exif_data)

    print("Exif data extraction complete. Output saved to 'exif_data.csv'")

# Replace 'folder_path' with the path to your folder containing the files
folder_path = r'C:\Users\admin\Desktop\Test'
get_exif_data(folder_path)
