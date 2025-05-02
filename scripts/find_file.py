import os

def filter_files_by_name(directory):
    """
    Delete files that do NOT contain the given name and display content of kept files.
    
    Args:
        directory (str): Directory path to search.
        name (str): Name to search for in files.
    """
    files_deleted = 0
    files_kept = 0
    name1 = "getme"
    name2 = "return"

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if name1 in content or name2 in content :
                        files_kept += 1
                        print(f"Keeping file (contains '{name1}' '{name2}'): {filename}")
                        print("--- Content ---")
                        print(content)
                        print("---------------\n")
                    else:
                        os.remove(filepath)  # Delete the file if name not found
                        files_deleted += 1
                        print(f"Deleted file (does not contain '{name1}' '{name2}'): {filename}")
            except UnicodeDecodeError:
                print(f"Skipping binary/unreadable file: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print(f"\nSummary: {files_kept} files kept, {files_deleted} files deleted.")

if __name__ == "__main__":
    directory = input("Enter the directory path to search: ").strip()
    filter_files_by_name(directory)