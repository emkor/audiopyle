from logging import Logger
from typing import Any, Dict, Optional

from audiopyle.lib.services.store_provider import JsonFileStore, StoreError
from audiopyle.lib.utils.file_system import PLUGIN_CONFIG_FILE_NAME


class PluginConfigProvider(object):
    def __init__(self, file_store: JsonFileStore, logger: Logger) -> None:
        self.file_store = file_store
        self.logger = logger
        self._cached = None  # type: Optional[Dict[str, Dict[str, Any]]]

    def get_all(self) -> Optional[Dict[str, Any]]:
        if self._cached is None:
            try:
                self._cached = self.file_store.read(PLUGIN_CONFIG_FILE_NAME)  # type: ignore
            except StoreError as e:
                self.logger.warning(str(e))
                self._cached = None
        return self._cached

    def get_for_plugin(self, plugin_full_key: str) -> Dict[str, Any]:
        full_config = self.get_all()
        return full_config.get(plugin_full_key, {}) if full_config is not None else {}
