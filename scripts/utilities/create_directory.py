import os

def create_directory_if_not_exists(directory_path):
    """Create a directory if it doesn't already exist."""
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        # print(f"Directory '{directory_path}' was created.")
    else:
        # print(f"Directory '{directory_path}' already exists.")
        pass