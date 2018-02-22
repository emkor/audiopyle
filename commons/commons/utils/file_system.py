import json
import os
import shutil

from typing import Text, List, Any, Dict

AUDIO_FILES_DIR = "/root/audio"
TMP_DIR = "/root/audio_tmp"
RESULTS_DIR = "/root/result"


def store_result_as_json(serializable_content: Dict[Text, Any], task_id: Text, file_suffix: Text) -> None:
    target_path = os.path.join(RESULTS_DIR, "{}-{}.json".format(task_id, file_suffix))
    if not file_exists(target_path):
        output_file = None
        try:
            with open(target_path, 'w') as output_file:
                json.dump(serializable_content, output_file)
        except Exception as e:
            if output_file is not None:
                output_file.close()
            raise ValueError("Could not store to file at {}: {}".format(target_path, e))
    else:
        raise ValueError("File at {} already exists: can not store content there.".format(target_path))


def file_exists(absolute_path: Text) -> bool:
    return os.path.exists(absolute_path)


def concatenate_paths(base_path: Text, file_name: Text) -> Text:
    return os.path.join(base_path, file_name)


def get_file_name(absolute_path: Text) -> Text:
    """Returns file name from an absolute path"""
    return os.path.basename(absolute_path)


def list_files(path: Text = "/") -> List[Text]:
    return [f for f in os.listdir(path) if os.path.isfile(concatenate_paths(path, f))]


def copy_file(source: Text, destination: Text) -> None:
    shutil.copy2(source, destination)


def extract_extension(file_path: Text) -> Text:
    return os.path.splitext(file_path)[1][1:].strip().lower()


def remove_file(file_path: Text) -> None:
    os.remove(file_path)


def file_size_bytes(absolute_path: Text) -> int:
    return os.path.getsize(absolute_path)
