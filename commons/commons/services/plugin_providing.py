from logging import Logger
from typing import Text, List, Optional, Any
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

    def build_plugin_from_key(self, key: Text) -> VampyPlugin:
        plugin_categories = self.vamp_interface.get_category_of(key)
        plugin_outputs = self.vamp_interface.get_outputs_of(key)
        library_file_name = get_file_name(get_library_for(key))
        return VampyPlugin(key=key, categories=plugin_categories, outputs=plugin_outputs,
                           library_file_name=library_file_name)

    def list_vampy_plugins(self) -> List[VampyPlugin]:
        """Returns list of VAMPy plugins available in OS"""
        return [self.build_plugin_from_key(key=k) for k in self.list_plugin_keys()]

    def list_plugin_keys(self) -> List[Text]:
        """Returns list of VAMPy plugin keys available under OS"""
        return [k for k in self.vamp_interface.list_plugins() if k not in self.black_list_plugin_key]

    def list_categories(self) -> List[Text]:
        """Returns list of categories from installed plugins"""
        all_categories = []
        for plugin in self.list_vampy_plugins():
            all_categories.extend(plugin.categories)
        return list(set(all_categories))
