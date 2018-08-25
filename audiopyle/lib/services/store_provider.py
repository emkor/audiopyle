import os
import json
import gzip
import lzma

from typing import Any, List, Dict, Union

from audiopyle.lib.models.file_meta import FileMeta
from audiopyle.lib.utils.conversion import utc_timestamp_to_datetime
from audiopyle.lib.utils.file_system import file_exists, concatenate_paths, remove_file, get_file_name, list_full_paths, \
    DEFAULT_FILE_PERMISSIONS, ENCODING_UTF_8
from audiopyle.lib.utils.logger import get_logger


class StoreError(Exception):
    pass


class FileStore(object):
    def __init__(self, base_dir: str, permissions: int = DEFAULT_FILE_PERMISSIONS) -> None:
        self.base_dir = base_dir
        self.permissions = permissions
        self.logger = get_logger()

    def store(self, file_name: str, content: Union[Dict[str, Any], List[Any]]) -> None:
        full_path = self._build_full_path(file_name)
        try:
            self._inherit_store(full_path, content)
            os.chmod(full_path, self.permissions)
        except Exception as e:
            message = "Could not store in {}: {}".format(full_path, e)
            self.logger.warning(message)
            raise StoreError(message)

    def read(self, file_name: str) -> Union[Dict[str, Any], List[Any]]:
        full_path = self._build_full_path(file_name)
        try:
            return self._inherit_read(full_path)
        except Exception as e:
            message = "Could not read from {}: {}".format(full_path, e)
            self.logger.warning(message)
            raise StoreError(message)

    def meta(self, file_name: str) -> FileMeta:
        file_name = self._build_full_path(file_name)
        file_stats = os.stat(file_name)
        last_access_utc = utc_timestamp_to_datetime(file_stats.st_atime)
        last_modification_utc = utc_timestamp_to_datetime(file_stats.st_mtime)
        created_on_utc = utc_timestamp_to_datetime(file_stats.st_ctime)
        return FileMeta(file_name=get_file_name(file_name), size=file_stats.st_size, last_access=last_access_utc,
                        last_modification=last_modification_utc, created_on=created_on_utc)

    def list(self) -> List[str]:
        """List file names (with extensions)"""
        return [get_file_name(f) for f in self.list_full_paths()]

    def list_full_paths(self) -> List[str]:
        """List file absolute paths (with extensions)"""
        return list_full_paths(self.base_dir)

    def get_full_path(self, file_name: str) -> str:
        return self._build_full_path(file_name)

    def remove(self, file_name: str) -> None:
        full_path = self._build_full_path(file_name)
        try:
            remove_file(full_path)
        except Exception as e:
            message = "Could not remove file {} because: {}".format(full_path, e)
            self.logger.warning(message)
            raise StoreError(message)

    def exists(self, file_name: str) -> bool:
        return file_exists(self._build_full_path(file_name))

    def _inherit_store(self, full_path: str, content: Union[Dict[str, Any], List[Any]]) -> None:
        raise NotImplementedError()

    def _inherit_read(self, full_path: str) -> Union[Dict[str, Any], List[Any]]:
        raise NotImplementedError()

    def _build_full_path(self, file_name: str) -> str:
        return concatenate_paths(self.base_dir, file_name)


class Mp3FileStore(FileStore):
    def __init__(self, base_dir: str) -> None:
        super().__init__(base_dir)

    def _inherit_read(self, full_path: str) -> Union[Dict[str, Any], List[Any]]:
        raise NotImplementedError()

    def _inherit_store(self, full_path: str, content: Union[Dict[str, Any], List[Any]]) -> None:
        raise NotImplementedError()


class JsonFileStore(FileStore):
    def __init__(self, base_dir: str) -> None:
        super().__init__(base_dir)

    def _inherit_store(self, full_path: str, content: Union[Dict[str, Any], List[Any]]):
        with open(full_path, "w") as output_file:
            json.dump(content, output_file)

    def _inherit_read(self, full_path: str) -> Union[Dict[str, Any], List[Any]]:
        with open(full_path, "r") as input_file:
            content = json.load(input_file)
        return content


class GzipJsonFileStore(FileStore):
    def __init__(self, base_dir: str) -> None:
        super().__init__(base_dir)

    def _inherit_store(self, full_path: str, content: Union[Dict[str, Any], List[Any]]):
        json_content = json.dumps(content).encode(ENCODING_UTF_8)
        with gzip.open(full_path, 'wb') as f:
            f.write(json_content)

    def _inherit_read(self, full_path: str) -> Union[Dict[str, Any], List[Any]]:
        with gzip.open(full_path, 'rb') as f:
            file_content = f.read()
        return json.loads(file_content.decode(ENCODING_UTF_8))


class LzmaJsonFileStore(FileStore):
    def __init__(self, base_dir: str) -> None:
        super().__init__(base_dir)

    def _inherit_store(self, full_path: str, content: Union[Dict[str, Any], List[Any]]):
        json_content = json.dumps(content).encode(ENCODING_UTF_8)
        with lzma.open(full_path, 'wb') as f:
            f.write(json_content)

    def _inherit_read(self, full_path: str) -> Union[Dict[str, Any], List[Any]]:
        with lzma.open(full_path, 'rb') as f:
            file_content = f.read()
        return json.loads(file_content.decode(ENCODING_UTF_8))
