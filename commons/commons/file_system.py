import os


def get_file_name(absolute_path):
    """
    Returns file name from an absolute path
    :type absolute_path: str
    :rtype: str
    """
    return os.path.basename(absolute_path)
