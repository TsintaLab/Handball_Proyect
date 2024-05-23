import os

# Define a function to remove the first 6 lines from a file
def remove_first_6_lines(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        lines = file.readlines()
    
    # Remove the first 6 lines
    new_lines = lines[6:]
    
    with open(file_path, 'w') as file:
        file.writelines(new_lines)

# Define the root directory where you have multiple 'tiro' directories
root_directory = 'Frames/Jugador3Sec3_2'

# Recursively iterate through all 'tiro' directories and their files
for root, dirs, files in os.walk(root_directory):
    for file_name in files:
        if file_name.endswith('.txt'):
            file_path = os.path.join(root, file_name)
            remove_first_6_lines(file_path)

print('Done')
