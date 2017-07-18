import os
import shutil

from os.path import isfile, join

AUDIO_FILES_DIR = "/audio"
TMP_DIR = "/audio_tmp"


def file_exists(absolute_path):
    """
    :type absolute_path: str
    :rtype: bool
    """
    return os.path.exists(absolute_path)


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


def copy_file(source, destination):
    """
    :type source: str
    :type destination: str
    """
    shutil.copy2(source, destination)


def extract_extension(file_path):
    """
    :type file_path: str
    :rtype: str
    """
    return os.path.splitext(file_path)[1][1:].strip()


def remove_file(file_path):
    """
    :type file_path: str
    """
    os.remove(file_path)
