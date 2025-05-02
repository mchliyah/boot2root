import os
import re
import shutil

def concatenate_ordered_files(directory):
    """
    1. Scan files for //fileXXX markers.
    2. Copy them to temporary filenames (fileXXX).
    3. Concatenate in order.
    4. Clean up temporary files.
    """
    file_pattern = re.compile(r'//file(\d+)')
    temp_files = []  # To track temporary files for cleanup

    # Step 1: Find all //fileXXX markers and copy files to temp names
    output_file= directory + "/output.c"
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    matches = file_pattern.findall(content)
                    if matches:
                        file_number = matches[0]  # e.g., "115"
                        temp_filename = f"file{file_number}"
                        temp_path = os.path.join(directory, temp_filename)
                        # Copy original file to temp name (e.g., file115)
                        shutil.copy2(filepath, temp_path)
                        temp_files.append(temp_path)
                        print(f"Copied: {filename} -> {temp_filename}")
            except (UnicodeDecodeError, ValueError) as e:
                print(f"Skipping {filename}: {e}")

    # Step 2: Read temp files in numerical order and concatenate
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for temp_path in sorted(temp_files, key=lambda x: int(re.search(r'file(\d+)', x).group(1))):
            try:
                with open(temp_path, 'r', encoding='utf-8') as file:
                    outfile.write(file.read() + "\n")
                    print(f"Added: {os.path.basename(temp_path)}")
            except Exception as e:
                print(f"Error reading {temp_path}: {e}")

    # Step 3: Clean up temporary files
    for temp_path in temp_files:
        try:
            os.remove(temp_path)
            print(f"Deleted temp file: {os.path.basename(temp_path)}")
        except Exception as e:
            print(f"Error deleting {temp_path}: {e}")

    print(f"\nDone. Output saved to {output_file}")

if __name__ == "__main__":
    directory = input("Enter directory path: ").strip()
    concatenate_ordered_files(directory)