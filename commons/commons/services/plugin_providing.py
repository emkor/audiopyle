from logging import Logger
from typing import Text, List, Optional, Any, Tuple
from vampyhost import get_library_for

import vamp

from commons.models.plugin import VampyPlugin
from commons.utils.file_system import get_file_name
from commons.utils.logger import get_logger


class VampyPluginProvider(object):
    def __init__(self, vamp_interface: Any = vamp, plugin_black_list: Optional[List[str]] = None,
                 logger: Optional[Logger] = None) -> None:
        self.vamp_interface = vamp_interface
        self.black_list_plugin_key = plugin_black_list or []
        self.logger = logger or get_logger()

    def build_plugins_from_key(self, vampy_key: Text) -> List[VampyPlugin]:
        vendor, name = self._split_vampy_key_into_vendor_and_name(vampy_key)
        plugin_outputs = self.vamp_interface.get_outputs_of(vampy_key)
        library_file_name = get_file_name(get_library_for(vampy_key))
        all_plugins = [VampyPlugin(vendor, name, o, library_file_name) for o in plugin_outputs]
        return [p for p in all_plugins if p.full_key not in self.black_list_plugin_key]

    def build_plugin_from_params(self, vendor: str, name: str, output: str) -> VampyPlugin:
        library_file_name = get_file_name(get_library_for("{}:{}".format(vendor, name)))
        return VampyPlugin(vendor, name, output, library_file_name)

    def build_plugin_from_full_key(self, full_plugin_key: str) -> VampyPlugin:
        vendor, name, output = self._split_full_key_into_params(full_plugin_key)
        return self.build_plugin_from_params(vendor, name, output)

    def list_full_plugin_keys(self) -> List[str]:
        full_key_list = []
        for k in self._list_vampy_plugin_keys():
            for o in self.vamp_interface.get_outputs_of(k):
                full_plugin_key = "{}:{}".format(k, o)
                if full_plugin_key not in self.black_list_plugin_key:
                    full_key_list.append(full_plugin_key)
        return full_key_list

    def list_vampy_plugins(self) -> List[VampyPlugin]:
        """Returns list of VAMPy plugins available in OS"""
        all_plugin = []
        for k in self._list_vampy_plugin_keys():
            new_plugins = self.build_plugins_from_key(k)
            all_plugin.extend(new_plugins)
        return all_plugin

    def _list_vampy_plugin_keys(self) -> List[Text]:
        """Returns list of VAMPy plugin keys available under OS"""
        return self.vamp_interface.list_plugins()

    def _split_vampy_key_into_vendor_and_name(self, vampy_key: str) -> Tuple[str, str]:
        vendor, _, name = vampy_key.partition(":")
        return vendor, name

    def _split_full_key_into_params(self, full_key: str) -> Tuple[str, str, str]:
        parts = full_key.split(":")
        return parts[0], parts[1], parts[2]
