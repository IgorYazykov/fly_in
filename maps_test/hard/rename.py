from pathlib import Path

def number_and_rename_files():
    directory = Path('.')
    
    # Get all files in the directory, sorted for consistent ordering
    files = sorted([f for f in directory.iterdir() if f.is_file() and f.name != 'rename.py'])
    
    for index, file_path in enumerate(files, start=1):
        # Format the number as a 2-digit string with '01', '02', etc., followed by '++'
        prefix = f"{index:02d}++"
        
        old_name = file_path.name
        new_name = prefix + old_name
        new_path = file_path.with_name(new_name)
        
        # Perform the rename
        file_path.rename(new_path)
        print(f"Renamed: {old_name} -> {new_name}")

if __name__ == '__main__':
    number_and_rename_files()