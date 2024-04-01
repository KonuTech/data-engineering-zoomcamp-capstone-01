import os


def print_project_structure(root_dir, indent=""):
    """
    Recursively print the project structure starting from the root directory,
    omitting specific directories (e.g., .git, .venv, __pycache__) and printing only directories.
    """
    if not os.path.exists(root_dir):
        print(f"Directory '{root_dir}' does not exist.")
        return

    # Print current directory
    print(indent + os.path.basename(root_dir) + "/")

    # Get list of subdirectories
    subdirs = [
        d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))
    ]
    subdirs.sort()

    # Directories to exclude
    exclude_dirs = [
        ".git",
        ".venv",
        "__pycache__",
        "logs",
    ]  # Add more directories here as needed

    # Recursive call for subdirectories
    for subdir in subdirs:
        subdir_path = os.path.join(root_dir, subdir)
        if subdir in exclude_dirs:
            continue  # Skip excluded directories
        print_project_structure(subdir_path, indent + "    ")


# Example usage:
print_project_structure(
    r"C:\\Users\\KonuTech\\projects\\data-engineering-zoomcamp-capstone-01\\"
)
