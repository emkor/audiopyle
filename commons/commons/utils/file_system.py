import os
import shutil

from typing import Text, List

from commons.utils.logger import get_logger

AUDIO_FILES_DIR = "/root/audio"
RESULTS_DIR = "/root/result"
DEFAULT_FILE_PERMISSIONS = 0o666
DEFAULT_DIR_PERMISSIONS = 0o777
ENCODING_UTF_8 = 'utf-8'

logger = get_logger()


def file_exists(absolute_path: Text) -> bool:
    return os.path.exists(absolute_path)


def concatenate_paths(base_path: Text, file_name: Text) -> Text:
    return os.path.join(base_path, file_name)


def get_file_name(absolute_path: Text) -> Text:
    """Returns file name from an absolute path"""
    return os.path.basename(absolute_path)


def list_full_paths(directory: Text = "/") -> List[Text]:
    return [os.path.join(directory, f)
            for f in os.listdir(directory) if os.path.isfile(concatenate_paths(directory, f))]


def list_files(path: Text = "/") -> List[Text]:
    return [f for f in os.listdir(path) if os.path.isfile(concatenate_paths(path, f))]


def copy_file(source: Text, destination: Text) -> None:
    shutil.copy2(source, destination)


def extract_extension(file_path: Text) -> Text:
    return os.path.splitext(file_path)[1][1:].strip().lower()


def extract_all_extensions(file_path: Text) -> Text:
    return file_path.partition('.')[2]


def remove_file(file_path: Text, ignore_errors: bool = False) -> None:
    try:
        os.remove(file_path)
    except:
        if ignore_errors:
            pass
        else:
            raise


def file_size_bytes(absolute_path: Text) -> int:
    return os.path.getsize(absolute_path)
