import os
import json
import gzip
import lzma

from typing import Text, Any, List, Dict

from commons.models.file_meta import FileMeta
from commons.utils.conversion import utc_timestamp_to_datetime
from commons.utils.file_system import file_exists, concatenate_paths, remove_file, get_file_name, \
    extract_all_extensions, list_full_paths, DEFAULT_FILE_PERMISSIONS, ENCODING_UTF_8
from commons.utils.logger import get_logger


class StoreError(Exception):
    pass


class FileStore(object):
    def __init__(self, base_dir: Text, extension: Text, permissions: int = DEFAULT_FILE_PERMISSIONS) -> None:
        self.base_dir = base_dir
        self.extension = extension
        self.permissions = permissions
        self.logger = get_logger()

    def store(self, identifier: Text, content: Dict[Text, Any]) -> None:
        full_path = self._build_full_path(identifier)
        try:
            self._inherit_store(full_path, content)
            os.chmod(full_path, self.permissions)
        except Exception as e:
            message = "Could not store in {}: {}".format(full_path, e)
            self.logger.warning(message)
            raise StoreError(message)

    def read(self, identifier: Text) -> Dict[Text, Any]:
        full_path = self._build_full_path(identifier)
        try:
            return self._inherit_read(full_path)
        except Exception as e:
            message = "Could not read from {}: {}".format(full_path, e)
            self.logger.warning(message)
            raise StoreError(message)

    def meta(self, identifier: Text) -> FileMeta:
        file_name = self._build_full_path(identifier)
        file_stats = os.stat(file_name)
        last_access_utc = utc_timestamp_to_datetime(file_stats.st_atime)
        last_modification_utc = utc_timestamp_to_datetime(file_stats.st_mtime)
        created_on_utc = utc_timestamp_to_datetime(file_stats.st_ctime)
        return FileMeta(file_name=get_file_name(file_name), size=file_stats.st_size, last_access=last_access_utc,
                        last_modification=last_modification_utc, created_on=created_on_utc)

    def list(self) -> List[Text]:
        """List file identifiers (file names without extensions)"""
        return [self._get_identifier(f) for f in self.list_file_names()]

    def list_file_names(self) -> List[Text]:
        """List file names (with extensions)"""
        return [get_file_name(f) for f in self.list_full_paths() if self._has_correct_extension(f)]

    def list_full_paths(self) -> List[Text]:
        """List file absolute paths (with extensions)"""
        return list_full_paths(self.base_dir)

    def get_full_path(self, identifier: Text) -> Text:
        return self._build_full_path(identifier)

    def remove(self, identifier: Text) -> None:
        full_path = self._build_full_path(identifier)
        try:
            remove_file(full_path)
        except Exception as e:
            message = "Could not remove file {} because: {}".format(full_path, e)
            self.logger.warning(message)
            raise StoreError(message)

    def exists(self, identifier: Text) -> bool:
        full_path = self._build_full_path(identifier)
        return file_exists(full_path) and extract_all_extensions(full_path).lower() == self.extension.lower()

    def _inherit_store(self, full_path: Text, content: Dict[Text, Any]) -> None:
        raise NotImplementedError()

    def _inherit_read(self, full_path: Text) -> Dict[Text, Any]:
        raise NotImplementedError()

    def _get_identifier(self, file_name: Text) -> Text:
        return file_name.partition('.')[0]

    def _has_correct_extension(self, file_path: Text) -> bool:
        return extract_all_extensions(file_path).lower() == self.extension.lower()

    def _build_full_path(self, identifier: Text) -> Text:
        return concatenate_paths(self.base_dir, self._build_file_name_with_ext(identifier))

    def _build_file_name_with_ext(self, identifier: Text) -> Text:
        return "{}.{}".format(identifier, self.extension)


class Mp3FileStore(FileStore):
    def __init__(self, base_dir: Text, permissions: int = DEFAULT_FILE_PERMISSIONS) -> None:
        super().__init__(base_dir, "mp3", permissions)

    def _inherit_read(self, full_path: Text) -> Dict[Text, Any]:
        with open(full_path, "r") as input_file:
            content = json.load(input_file)
        return content

    def _inherit_store(self, full_path: Text, content: Dict[Text, Any]) -> None:
        raise NotImplementedError()


class JsonFileStore(FileStore):
    def __init__(self, base_dir: Text, permissions: int = DEFAULT_FILE_PERMISSIONS) -> None:
        super().__init__(base_dir, "json", permissions)

    def _inherit_store(self, full_path: Text, content: Dict[Text, Any]):
        with open(full_path, "w") as output_file:
            json.dump(content, output_file)

    def _inherit_read(self, full_path: Text) -> Dict[Text, Any]:
        with open(full_path, "r") as input_file:
            content = json.load(input_file)
        return content


class GzipJsonFileStore(FileStore):
    def __init__(self, base_dir: Text, permissions: int = DEFAULT_FILE_PERMISSIONS) -> None:
        super().__init__(base_dir, "json.gzip", permissions)

    def _inherit_store(self, full_path: Text, content: Dict[Text, Any]):
        json_content = json.dumps(content).encode(ENCODING_UTF_8)
        with gzip.open(full_path, 'wb') as f:
            f.write(json_content)

    def _inherit_read(self, full_path: Text) -> Dict[Text, Any]:
        with gzip.open(full_path, 'rb') as f:
            file_content = f.read()
        return json.loads(file_content.decode(ENCODING_UTF_8))


class LzmaJsonFileStore(FileStore):
    def __init__(self, base_dir: Text, extension: Text = "json.lzma") -> None:
        super().__init__(base_dir, extension)

    def _inherit_store(self, full_path: Text, content: Dict[Text, Any]):
        json_content = json.dumps(content).encode(ENCODING_UTF_8)
        with lzma.open(full_path, 'wb') as f:
            f.write(json_content)

    def _inherit_read(self, full_path: Text) -> Dict[Text, Any]:
        with lzma.open(full_path, 'rb') as f:
            file_content = f.read()
        return json.loads(file_content.decode(ENCODING_UTF_8))
