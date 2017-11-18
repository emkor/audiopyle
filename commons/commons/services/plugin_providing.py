from typing import Text, List, Optional
from vampyhost import get_library_for

import vamp

from commons.models.plugin import VampyPlugin


def build_plugin_from_key(key: Text) -> VampyPlugin:
    plugin_categories = vamp.get_category_of(key)
    plugin_outputs = vamp.get_outputs_of(key)
    library_file = get_library_for(key)
    return VampyPlugin(key=key, categories=plugin_categories, outputs=plugin_outputs, library_path=library_file)


def list_vampy_plugins(blacklisted_plugin_keys: Optional[List[Text]] = None) -> List[VampyPlugin]:
    """Returns list of VAMPy plugins available in OS"""
    return [build_plugin_from_key(key=k) for k in vamp.list_plugins() if k not in (blacklisted_plugin_keys or [])]


def list_categories(plugins: List[VampyPlugin]) -> List[Text]:
    """Returns list of categories from installed plugins"""
    all_categories = []
    for plugin in plugins:
        all_categories.extend(plugin.categories)
    return list(set(all_categories))
