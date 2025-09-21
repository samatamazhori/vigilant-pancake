
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


def remove_file_by_name(root_dir: str, filename_to_delete: str):
    """
    Recursively finds and removes all files matching a specific name within a directory tree.

    This function traverses the directory structure starting from `root_dir` and
    deletes any file that has an exact match with `filename_to_delete`. It logs each
    action and provides a summary upon completion.

    Args:
        root_dir (str): The absolute or relative path to the root directory
                        to start the search and removal process. The function will
                        log an error and exit if this path does not exist.
        filename_to_delete (str): The exact name of the file to be deleted
                                  (e.g., 'config.yml', 'temp_data.csv').

    Returns:
        int: The total number of files that were successfully removed.

    Raises:
        FileNotFoundError: If the specified `root_dir` does not exist.
        ValueError: If `filename_to_delete` is empty or None.
    """
    print(f"Initiating search for file '{filename_to_delete}' to remove within '{root_dir}'.")

    # --- 1. Input Validation ---
    if not os.path.isdir(root_dir):
        print(f"The specified root directory '{root_dir}' does not exist or is not a directory.")
        raise FileNotFoundError(f"The specified root directory '{root_dir}' does not exist.")

    if not filename_to_delete or not filename_to_delete.strip():
        print("The 'filename_to_delete' argument cannot be empty.")
        raise ValueError("The 'filename_to_delete' argument cannot be empty.")

    removed_count = 0
    scanned_count = 0

    # --- 2. Directory Traversal and File Removal ---
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Safety Check: Do not traverse or modify the .git directory.
        if '.git' in dirnames:
            dirnames.remove('.git')
            print(f"Skipping '.git' directory found in '{dirpath}'.")

        # Check if the target file is in the list of files for the current directory
        if filename_to_delete in filenames:
            file_path = os.path.join(dirpath, filename_to_delete)
            try:
                os.remove(file_path)
                print(f"Removed file: {file_path}")
                removed_count += 1
            except IsADirectoryError:
                # This can happen if a directory has the same name as the file we want to delete.
                print(f"A directory was found at '{file_path}' with the same name. Skipping.")
            except OSError as e:
                # Log other OS-level errors (e.g., permission denied)
                print(f"Error removing file {file_path}: {e}")
            except Exception as e:
                print(f"An unexpected error occurred while trying to remove {file_path}: {e}")
        
        scanned_count += len(filenames)

    # --- 3. Final Summary ---
    if removed_count > 0:
        print(f"Process complete. Scanned {scanned_count} files and removed {removed_count} instance(s) of '{filename_to_delete}'.")
    else:
        print(f"Process complete. Scanned {scanned_count} files. No file named '{filename_to_delete}' was found.")
        
    return removed_count




if __name__ == '__main__':
    # Example Usage for renaming the dotnet project
    test_dir = "test_dotnet"
    placeholder = "cad.template."
    new_name = "cad.kir."

    print(f"--- Renaming files and directories in {test_dir} ---")
    rename_files_and_dirs(test_dir, placeholder, new_name)

    print(f"\n--- Replacing content in files in {test_dir} ---")
    replace_content_in_files(test_dir, placeholder, new_name)

