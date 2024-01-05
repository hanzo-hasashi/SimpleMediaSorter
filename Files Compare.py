# Compares files between two directories

import os
from config_media_sorter import source_directory_para, destination_directory_para

# # Define the two directories to compare
dir1 = r'C:\Users\admin\Downloads\Takeout\Takeout\Google Photos'
dir2 = r'E:\Media\PhotoSpace'

# # Use Source & Destination from config_media_sorter.py file
# dir1 = source_directory_para
# dir2 = destination_directory_para

# Get the list of files in each directory
files_in_dir1 = os.listdir(dir1)
files_in_dir2 = os.listdir(dir2)

# Convert the lists to sets for efficient comparison
set1 = set(files_in_dir1)
set2 = set(files_in_dir2)

# Find files that are unique to each directory
unique_to_dir1 = set1 - set2
unique_to_dir2 = set2 - set1

# # Display the results
# print("Files unique to directory 1: ", dir1)
# for file in unique_to_dir1:
#     print(os.path.join(dir1, file))

print("\nFiles unique to directory 2: ", dir2)
for file in unique_to_dir2:
    print(os.path.join(dir2, file))

# # Check for common files (files present in both directories)
# common_files = set1.intersection(set2)
# if common_files:
#     print("\nCommon files in both directories:")
#     for file in common_files:
#         print(file)
# else:
#     print("\nNo common files found between the directories.")
