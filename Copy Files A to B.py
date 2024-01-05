import csv
import shutil
import os

# Initialize lists to track successful and unsuccessful moves
successful_moves = []
unsuccessful_moves = []

# Path to the CSV file
csv_file = r"C:\Users\admin\Videos\source_destination_info.csv"

# Check if the CSV file exists
if not os.path.exists(csv_file):
    print(f"Error: The CSV file '{csv_file}' does not exist.")
else:
    # Open and read the CSV file
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) != 2:
                print(f"Skipping invalid line in CSV: {row}")
                continue
            
            source = row[0].strip()
            destination = row[1].strip()

            # Check if the source file exists
            if os.path.exists(source):
                try:
                    # Attempt to move the file to the destination
                    shutil.move(source, destination)
                    successful_moves.append(source)
                except Exception as e:
                    unsuccessful_moves.append((source, destination, str(e)))
            else:
                unsuccessful_moves.append((source, destination, "Source file not found"))

# Print the summary
print("\nSummary:")
print("Files successfully moved:")
for file in successful_moves:
    print(file)

print("\nFiles not moved (with reasons):")
for move_error in unsuccessful_moves:
    print(f"Source: {move_error[0]}, Destination: {move_error[1]}, Reason: {move_error[2]}")
