import os

def remove_lines_with_name(directory, name):
    """
    Remove lines containing 'name' from all files in 'directory'.
    
    Args:
        directory (str): Path to the directory containing files.
        name (str): Name to search for and remove lines.
    """
    files_processed = 0
    lines_removed = 0

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    lines = file.readlines()  # Read all lines
                
                # Filter out lines containing the name (case-sensitive)
                new_lines = [line for line in lines if name not in line]
                
                # If some lines were removed, overwrite the file
                if len(new_lines) < len(lines):
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.writelines(new_lines)
                    removed = len(lines) - len(new_lines)
                    lines_removed += removed
                    print(f"Removed {removed} lines from: {filename}")
                    files_processed += 1
            except UnicodeDecodeError:
                print(f"Skipping binary/unreadable file: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"\nDone. Removed {lines_removed} lines across {files_processed} files.")

if __name__ == "__main__":
    directory = input("Enter directory path: ").strip()
    name = input("Enter name to remove lines containing it: ").strip()
    remove_lines_with_name(directory, name)