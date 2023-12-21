def readQssFile(qss_file_path, encoding='utf-8'):
    """
    Read and return the content of a QSS file using the specified encoding.

    Args:
        qss_file_path (str): The path to the QSS file.
        encoding (str): The encoding used to read the file. Defaults to 'utf-8'.

    Returns:
        str: The content of the QSS file.

    Raises:
        FileNotFoundError: If the QSS file does not exist.
        IOError: If there is an error reading the file.
        UnicodeDecodeError: If decoding the file fails.
    """
    try:
        with open(qss_file_path, 'r', encoding=encoding) as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {qss_file_path}")
    except IOError as e:
        raise IOError(f"Error reading file {qss_file_path}: {e}")
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(f"Error decoding file {qss_file_path} with encoding {encoding}: {e}")

