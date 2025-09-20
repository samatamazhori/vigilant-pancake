
import os
import shutil

def rename_files_and_dirs(root_dir, placeholder, new_string):
    """
    Recursively renames files and directories by replacing a placeholder string.

    Args:
        root_dir (str): The root directory to start the renaming process.
        placeholder (str): The placeholder string to be replaced.
        new_string (str): The new string to replace the placeholder.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=False):
        # Rename files
        for filename in filenames:
            if placeholder in filename:
                old_path = os.path.join(dirpath, filename)
                new_filename = filename.replace(placeholder, new_string)
                new_path = os.path.join(dirpath, new_filename)
                try:
                    shutil.move(old_path, new_path)
                    print(f"Renamed file: {old_path} -> {new_path}")
                except IOError as e:
                    print(f"Error renaming file {old_path}: {e}")

        # Rename directories
        for dirname in dirnames:
            if placeholder in dirname:
                old_path = os.path.join(dirpath, dirname)
                new_dirname = dirname.replace(placeholder, new_string)
                new_path = os.path.join(dirpath, new_dirname)
                try:
                    shutil.move(old_path, new_path)
                    print(f"Renamed directory: {old_path} -> {new_path}")
                except IOError as e:
                    print(f"Error renaming directory {old_path}: {e}")

def replace_content_in_files(root_dir, old_string, new_string, file_extensions=None):
    """
    Recursively replaces content in files.

    Args:
        root_dir (str): The root directory to start the replacement process.
        old_string (str): The string to be replaced.
        new_string (str): The new string to replace the old string.
        file_extensions (list, optional): A list of file extensions to process.
                                          If None, all files are processed.
                                          Example: ['.txt', '.py']
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if file_extensions:
                if not any(filename.endswith(ext) for ext in file_extensions):
                    continue

            file_path = os.path.join(dirpath, filename)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    file_content = file.read()

                if old_string in file_content:
                    new_content = file_content.replace(old_string, new_string)
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f"Replaced content in: {file_path}")
            except IOError as e:
                print(f"Error processing file {file_path}: {e}")

def remove_files_by_extension(root_dir, extension):
    """
    Recursively removes files with a specific extension.

    Args:
        root_dir (str): The root directory to start the removal process.
        extension (str): The file extension to remove (e.g., '.txt', '.log').
    """
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(extension):
                file_path = os.path.join(dirpath, filename)
                try:
                    os.remove(file_path)
                    print(f"Removed file: {file_path}")
                except OSError as e:
                    print(f"Error removing file {file_path}: {e}")

if __name__ == '__main__':
    # Example Usage for renaming the dotnet project
    test_dir = "test_dotnet"
    placeholder = "cad.template."
    new_name = "cad.kir."

    print(f"--- Renaming files and directories in {test_dir} ---")
    rename_files_and_dirs(test_dir, placeholder, new_name)

    print(f"\n--- Replacing content in files in {test_dir} ---")
    replace_content_in_files(test_dir, placeholder, new_name)

