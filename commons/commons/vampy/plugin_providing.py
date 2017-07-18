import vamp
from vampyhost import get_library_for

from commons.vampy.plugin import VampyPlugin


def build_plugin_from_key(key):
    """
    :type key: str
    :rtype: commons.vampy.plugin.VampyPlugin
    """
    plugin_categories = vamp.get_category_of(key)
    plugin_outputs = vamp.get_outputs_of(key)
    library_file = get_library_for(key)
    return VampyPlugin(key=key, categories=plugin_categories, outputs=plugin_outputs, library_path=library_file)


def list_vampy_plugins():
    """
    Returns list of VAMPy plugins available in OS
    :rtype: list[commons.vampy.plugin.VampyPlugin]
    """
    return list(map(lambda key: build_plugin_from_key(key=key), vamp.list_plugins()))


def list_categories(plugins):
    """
    Returns list of categories from installed plugins.
    :type plugins: list[commons.vampy.plugin.VampyPlugin]
    :rtype: list[str]
    """
    all_categories = []
    for plugin in plugins:
        all_categories.extend(plugin.categories)
    return list(set(all_categories))
