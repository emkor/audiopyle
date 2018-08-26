import os
import shutil

from typing import List

from audiopyle.lib.utils.logger import get_logger

AUDIO_FILES_DIR = "/home/audiopyle/audio"
CONFIG_DIR = "/home/audiopyle/config"
PLUGIN_CONFIG_FILE_NAME = "plugin.json"
PLUGIN_BLACKLIST_CONFIG_FILE_NAME = "blacklist.json"
METRIC_CONFIG_FILE_NAME = "metric.json"
DEFAULT_FILE_PERMISSIONS = 0o666
DEFAULT_DIR_PERMISSIONS = 0o777
ENCODING_UTF_8 = 'utf-8'


logger = get_logger()


def file_exists(absolute_path: str) -> bool:
    return os.path.exists(absolute_path)


def concatenate_paths(base_path: str, file_name: str) -> str:
    return os.path.join(base_path, file_name)


def get_file_name(absolute_path: str) -> str:
    """Returns file name from an absolute path"""
    return os.path.basename(absolute_path)


def list_full_paths(directory: str = "/") -> List[str]:
    return [os.path.join(directory, f)
            for f in os.listdir(directory) if os.path.isfile(concatenate_paths(directory, f))]


def list_files(path: str = "/") -> List[str]:
    return [f for f in os.listdir(path) if os.path.isfile(concatenate_paths(path, f))]


def copy_file(source: str, destination: str) -> None:
    shutil.copy2(source, destination)


def extract_extension(file_path: str) -> str:
    return os.path.splitext(file_path)[1][1:].strip().lower()


def extract_all_extensions(file_path: str) -> str:
    return file_path.partition('.')[2]


def remove_file(file_path: str, ignore_errors: bool = False) -> None:
    try:
        os.remove(file_path)
    except Exception as e:
        if ignore_errors:
            pass
        else:
            raise e


def file_size_bytes(absolute_path: str) -> int:
    return os.path.getsize(absolute_path)
