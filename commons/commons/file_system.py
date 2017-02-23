import os

from os.path import isfile, join


def get_file_name(absolute_path):
    """
    Returns file name from an absolute path
    :type absolute_path: str
    :rtype: str
    """
    return os.path.basename(absolute_path)


def list_files(path="/"):
    """
    :type path: str
    :rtype: list[str]
    """
    return [f for f in os.listdir(path) if isfile(join(path, f))]
