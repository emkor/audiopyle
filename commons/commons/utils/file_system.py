import os
import shutil

from typing import Text, List

AUDIO_FILES_DIR = "/audio"
TMP_DIR = "/audio_tmp"


def file_exists(absolute_path: Text) -> bool:
    return os.path.exists(absolute_path)


def concatenate_paths(base_path: Text, file_name: Text) -> Text:
    return os.path.join(base_path, file_name)


def get_file_name(absolute_path: Text) -> Text:
    """Returns file name from an absolute path"""
    return os.path.basename(absolute_path)


def list_files(path: Text = "/") -> List[Text]:
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]


def copy_file(source: Text, destination: Text) -> None:
    shutil.copy2(source, destination)


def extract_extension(file_path: Text) -> Text:
    return os.path.splitext(file_path)[1][1:].strip().lower()


def remove_file(file_path: Text) -> None:
    os.remove(file_path)


def file_size_bytes(absolute_path: Text) -> int:
    return os.path.getsize(absolute_path)
