from logging import Logger
from typing import Any, Dict, Optional

from commons.services.store_provider import JsonFileStore, StoreError
from commons.utils.file_system import METRIC_CONFIG_IDENTIFIER


class MetricConfigProvider(object):
    def __init__(self, file_store: JsonFileStore, logger: Logger) -> None:
        self.file_store = file_store
        self.logger = logger

    def get_all(self) -> Optional[Dict[str, Any]]:
        try:
            return self.file_store.read(METRIC_CONFIG_IDENTIFIER)  # type: ignore
        except StoreError as e:
            self.logger.warning(str(e))
            return None

    def get_for_plugin(self, plugin_full_key: str) -> Dict[str, Any]:
        plugin_config = {}
        full_config = self.get_all() or {}
        for metric_name, metric_config in full_config.items():
            if plugin_full_key == metric_config["plugin"]:
                metric_config.pop("plugin")
                plugin_config.update({metric_name: metric_config})
        return plugin_config

    def get_by_name(self, metric_name):
        full_config = self.get_all()
        return full_config.get(metric_name, {}) if full_config is not None else {}
