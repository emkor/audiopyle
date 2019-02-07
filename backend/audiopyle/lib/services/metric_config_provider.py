from logging import Logger
from typing import Any, Dict, Optional, List

from audiopyle.lib.services.store_provider import JsonFileStore, StoreError
from audiopyle.lib.utils.file_system import METRIC_CONFIG_FILE_NAME


class MetricConfigProvider(object):
    def __init__(self, file_store: JsonFileStore, logger: Logger) -> None:
        self.file_store = file_store
        self.logger = logger
        self._cached = None  # type: Optional[Dict[str, Dict[str, Any]]]

    def get_all(self) -> Optional[Dict[str, Any]]:
        if self._cached is None:
            try:
                self._cached = self.file_store.read(METRIC_CONFIG_FILE_NAME)  # type: ignore
            except StoreError as e:
                self.logger.warning(str(e))
                self._cached = None
        return self._cached

    def get_for_plugin(self, plugin_full_key: str) -> Dict[str, Any]:
        plugin_config = {}
        full_config = self.get_all() or {}
        for metric_name, metric_config in full_config.items():
            if plugin_full_key == metric_config["plugin"]:
                plugin_config.update({metric_name: metric_config})
        return plugin_config

    def get_by_name(self, metric_name) -> Dict[str, Any]:
        full_config = self.get_all() or {}
        return full_config.get(metric_name, {})

    def get_metric_names(self) -> List[str]:
        full_config = self.get_all() or {}
        return list(full_config.keys())

    def get_metric_names_for_plugin(self, plugin_full_key: str) -> List[str]:
        metric_names = []
        for metric_name, metric_config in (self.get_all() or {}).items():
            if plugin_full_key == metric_config["plugin"]:
                metric_names.append(metric_name)
        return metric_names
