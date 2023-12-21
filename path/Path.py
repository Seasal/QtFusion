# QtFusion, AGPL-3.0 license
import inspect
import os
import shutil
from typing import List, Optional
"""
Path Package: Simplified File and Directory Operations in QtFusion

The 'path' package offers a set of functions to facilitate file and directory handling in Python. 
Designed for ease of use and efficiency, this package includes utilities for common path operations 
suitable for a variety of applications, from simple file management tasks to more complex file 
system manipulations.

Features:
- Path existence checking with 'path_exists'.
- Directory creation with 'create_dir'.
- Listing directory contents via 'list_dir'.
- File extension retrieval with 'get_extension'.
- Path concatenation using 'join_paths'.
- Conversion of relative to absolute paths in 'to_abs_path'.
- Filename extraction without extension through 'get_filename'.
- Size calculation for files and directories using 'get_size'.
- File copying with 'copy_file'.
- File or directory moving/renaming through 'move_or_rename'.
- More features will be added in future updates.

This toolkit is crafted to be intuitive and cross-platform, streamlining file system operations 
across different environments and applications.
"""


def get_abs_path(base_path: Optional[str] = None, *relative_paths: str) -> str:
    """
    Appends an absolute path prefix to a set of relative paths.

    Args:
        base_path (Optional[str]): The base path. If None, the script's absolute path is used by default.
        *relative_paths (str): A set of relative path strings.

    Returns:
        str: The combined absolute path.

    Raises:
        ValueError: If the provided path is invalid.
    """
    # Use the script's directory as the default base path
    if base_path is None:
        # Get the file path of the caller
        caller_frame = inspect.stack()[1]
        caller_path = caller_frame.filename
        base_path = os.path.dirname(os.path.abspath(caller_path))

    # On Windows, remove leading slashes from each relative path
    cleaned_relative_paths = [os.path.normpath(p.lstrip('/\\')) if os.name == 'nt' else p for p in relative_paths]

    # Combine the cleaned relative paths
    combined_relative_path = os.path.join(*cleaned_relative_paths)

    # Join the base path with the combined relative path
    absolute_path = os.path.join(base_path, combined_relative_path)

    # Normalize the path
    absolute_path = os.path.normpath(absolute_path)

    return absolute_path


def abs_path(relative_path: str, base_path: Optional[str] = None, path_type: Optional[str] = "current") -> str:
    """
    Appends an absolute path prefix to a single relative path.

    Args:
        relative_path (str): The relative path string.
        base_path (Optional[str]): The base path. If None, the path is determined based on path_type.
        path_type (Optional[str]): The type of base path to use.
                                   "current" for the caller's file directory,
                                   "project" for the project's root directory,
                                   or "parent" for the parent directory of the caller's file.

    Returns:
        str: The combined absolute path.

    Raises:
        ValueError: If the provided path is invalid.
    """
    if base_path is None:
        # Get the file path of the caller
        caller_frame = inspect.stack()[1]
        caller_path = caller_frame.filename
        caller_dir = os.path.dirname(os.path.abspath(caller_path))

        if path_type == "current":
            base_path = caller_dir
        elif path_type == "project":
            # Assuming the project directory is the first directory without __init__.py
            while os.path.exists(os.path.join(caller_dir, '../__init__.py')):
                caller_dir = os.path.dirname(caller_dir)
            base_path = caller_dir
        elif path_type == "parent":
            base_path = os.path.dirname(caller_dir)
        else:
            raise ValueError(f"Invalid path_type '{path_type}'. Expected 'current', 'project', or 'parent'.")

    # Normalize the relative path
    cleaned_relative_path = os.path.normpath(relative_path.lstrip('/\\')) if os.name == 'nt' else relative_path

    # Join the base path with the relative path
    absolute_path = os.path.join(base_path, cleaned_relative_path)

    # Normalize the path
    absolute_path = os.path.normpath(absolute_path)

    return absolute_path


def get_files(prefix: str, paths: List[str]) -> List[str]:
    """
    Get all files using a specified prefix and list of paths.

    Args:
        prefix (str): The path prefix.
        paths (List[str]): List of paths.

    Returns:
        List[str]: List of file paths.
    """
    abs_paths = [os.path.join(prefix, path) for path in paths]
    return list_all_files(abs_paths)


def list_all_files(paths: List[str]) -> List[str]:
    """
    List all files from multiple directories.

    Args:
        paths (List[str]): List of directory paths.

    Returns:
        List[str]: List of file paths.
    """
    files = []
    for path in paths:
        files.extend(list_files(path))
    return files


def list_files(path: str) -> List[str]:
    """
    List all files in a specified directory.

    Args:
        path (str): Directory path.

    Returns:
        List[str]: List of file paths.
    """
    # Use os.scandir for efficiency in large directories
    return sorted([
        os.path.abspath(os.path.join(path, entry.name))
        for entry in os.scandir(path)
        if entry.is_file() and not entry.name.startswith(".")
    ])


def path_exists(path: str) -> bool:
    """
    Checks if the specified path exists.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    return os.path.exists(path)


def create_dir(path: str, exist_ok: bool = True) -> None:
    """
    Creates a new directory at the specified path.

    Args:
        path (str): The directory path to create.
        exist_ok (bool): If True, does not raise an exception if the directory already exists.

    """
    os.makedirs(path, exist_ok=exist_ok)


def list_dir(path: str) -> list:
    """
    Lists files and directories in the given path.

    Args:
        path (str): The directory path to list contents of.

    Returns:
        list: List of files and directories in the given path.
    """
    return os.listdir(path)


def get_extension(filename: str) -> str:
    """
    Returns the file extension of the specified file.

    Args:
        filename (str): The filename to get the extension of.

    Returns:
        str: The file extension.
    """
    return os.path.splitext(filename)[1]


def join_paths(*paths: str) -> str:
    """
    Joins multiple paths into a single path.

    Args:
        *paths (str): Paths to be joined.

    Returns:
        str: The combined path.
    """
    return os.path.join(*paths)


def to_abs_path(relative_path: str) -> str:
    """
    Converts a relative path to an absolute path.

    Args:
        relative_path (str): The relative path to convert.

    Returns:
        str: The absolute path.
    """
    return os.path.abspath(relative_path)


def get_script_dir():
    """
    Get the directory of the current executing script.

    Returns:
        str: The absolute path of the directory containing the current script.
    """
    # Get the file path of the current script
    caller_frame = inspect.stack()[1]
    script_path = caller_frame.filename
    script_dir = os.path.dirname(os.path.abspath(script_path))

    return script_dir


def get_script_path():
    """
    Get the absolute path of the current executing script.

    Returns:
        str: The absolute path of the current script.
    """
    # Get the file path of the current script
    caller_frame = inspect.stack()[1]
    script_path = os.path.abspath(caller_frame.filename)

    return script_path


def get_filename(path: str) -> str:
    """
    Returns the filename without its extension from the given path.

    Args:
        path (str): The file path.

    Returns:
        str: The filename without its extension.
    """
    return os.path.splitext(os.path.basename(path))[0]


def get_size(path: str) -> int:
    """
    Returns the size of the file or directory at the specified path.

    Args:
        path (str): The path of the file or directory.

    Returns:
        int: The size in bytes.
    """
    if os.path.isfile(path):
        return os.path.getsize(path)
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)
    return total_size


def copy_file(src: str, dest: str) -> None:
    """
    Copies a file from the source to the destination.

    Args:
        src (str): The source file path.
        dest (str): The destination file path.
    """
    shutil.copy2(src, dest)


def move_or_rename(src: str, dest: str) -> None:
    """
    Moves or renames a file or directory.

    Args:
        src (str): The source file or directory path.
        dest (str): The destination file or directory path.
    """
    shutil.move(src, dest)
