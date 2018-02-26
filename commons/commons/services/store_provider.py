import gzip
import json
from logging import getLogger

from typing import Text, Any, List, Dict, Optional
from enum import Enum

from commons.utils.file_system import file_exists, concatenate_paths, remove_file, list_files, extract_extension, \
    get_file_name, extract_all_extensions


class FileMode(Enum):
    binary = "b"
    text = "t"


class FileStore(object):
    def __init__(self, base_dir: Text, extension: Text) -> None:
        self.base_dir = base_dir
        self.extension = extension
        self.logger = getLogger()

    def store(self, file_name: Text, content: Dict[Text, Any]) -> bool:
        full_path = self._build_full_path(file_name)
        try:
            self._inherit_store(full_path, content)
            return True
        except Exception as e:
            self.logger.warning("Could not store in {}: {}".format(full_path, e))
            return False

    def read(self, file_name: Text) -> Optional[Dict[Text, Any]]:
        full_path = self._build_full_path(file_name)
        try:
            return self._inherit_read(full_path)
        except Exception as e:
            self.logger.warning("Could not read from {}: {}".format(full_path, e))
            return None

    def list(self) -> List[Text]:
        all_files = list_files(self.base_dir)
        file_names = [get_file_name(f) for f in all_files if self._has_correct_extension(f)]
        return [self._strip_just_name(f) for f in file_names]

    def remove(self, file_name: Text) -> bool:
        full_path = self._build_full_path(file_name)
        try:
            remove_file(full_path)
            return True
        except Exception as e:
            self.logger.warning("Could not remove file {} because: {}".format(full_path, e))
            return False

    def exists(self, file_name: Text) -> bool:
        full_path = self._build_full_path(file_name)
        return file_exists(full_path) and extract_all_extensions(full_path).lower() == self.extension.lower()

    def _inherit_store(self, full_path: Text, content: Dict[Text, Any]) -> None:
        raise NotImplementedError()

    def _inherit_read(self, full_path: Text) -> Dict[Text, Any]:
        raise NotImplementedError()

    def _strip_just_name(self, file_name_with_extensions: Text) -> Text:
        return file_name_with_extensions.partition('.')[0]

    def _has_correct_extension(self, file_path: Text) -> bool:
        return extract_all_extensions(file_path).lower() == self.extension.lower()

    def _build_full_path(self, file_name: Text) -> Text:
        return concatenate_paths(self.base_dir, self._build_file_name_with_ext(file_name))

    def _build_file_name_with_ext(self, file_name: Text) -> Text:
        return "{}.{}".format(file_name, self.extension)


class JsonFileStore(FileStore):
    def __init__(self, base_dir: Text) -> None:
        super().__init__(base_dir, "json")

    def _inherit_store(self, full_path: Text, content: Dict[Text, Any]):
        with open(full_path, "w") as output_file:
            json.dump(content, output_file)

    def _inherit_read(self, full_path: Text) -> Dict[Text, Any]:
        with open(full_path, "r") as input_file:
            content = json.load(input_file)
        return content


class GzipJsonFileStore(FileStore):
    def __init__(self, base_dir: Text) -> None:
        super().__init__(base_dir, "json.gzip")

    def _inherit_store(self, full_path: Text, content: Dict[Text, Any]):
        json_content = json.dumps(content).encode('utf-8')
        with gzip.open(full_path, 'wb') as f:
            f.write(json_content)

    def _inherit_read(self, full_path: Text) -> Dict[Text, Any]:
        with gzip.open(full_path, 'rb') as f:
            file_content = f.read()
        return json.loads(file_content.decode('utf-8'))
