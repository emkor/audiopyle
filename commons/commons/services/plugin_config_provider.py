from logging import Logger
from typing import Any, Dict, Optional

from commons.services.store_provider import JsonFileStore, StoreError
from commons.utils.file_system import PLUGIN_CONFIG_IDENTIFIER


class PluginConfigProvider(object):
    def __init__(self, file_store: JsonFileStore, logger: Logger) -> None:
        self.file_store = file_store
        self.logger = logger

    def get_all(self) -> Optional[Dict[str, Any]]:
        try:
            return self.file_store.read(PLUGIN_CONFIG_IDENTIFIER)  # type: ignore
        except StoreError as e:
            self.logger.warning(str(e))
            return None

    def get_for_plugin(self, plugin_full_key: str) -> Dict[str, Any]:
        full_config = self.get_all()
        return full_config.get(plugin_full_key, {}) if full_config is not None else {}
