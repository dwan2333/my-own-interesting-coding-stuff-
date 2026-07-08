from pathlib import Path

def is_valid_path(path_str):
    p = Path(path_str)
    
    # 0. Check if the path is an absolute path (starts with a drive letter like D:\ or C:\)
    if not p.is_absolute():
        print("Error: You must provide a full, absolute path (e.g., D:\\my_quiz_folder).")
        return False
        
    p = p.resolve()
    
    # 1. Check if the drive/root actually exists (e.g., making sure D:\ exists)
    if not Path(p.anchor).exists():
        print(f"Error: The drive {p.anchor} does not exist.")
        return False
        
    # 2. Check for invalid Windows characters in the folder names
    invalid_chars = '<>:"|?*'
    for part in p.parts[1:]: # skip the drive letter when checking
        if any(char in invalid_chars for char in part):
            print("Error: Path contains invalid characters (< > : \" | ? *).")
            return False
            
    # 3. Check if the path already points to an existing file
    if p.is_file():
        print("Error: That path already points to a file, not a folder.")
        return False
        
    return True

while True:
    user_input = input("Enter the path for the quiz folder: ")
    
    if is_valid_path(user_input):
        quiz_folder = Path(user_input)
        print(f"Success! '{quiz_folder}' is a valid path format to use later.")
        break
    else:
        print("Please try again.\n")

print(quiz_folder)


