import vamp

from xtracter.model.vampy_plugin import VampyPlugin
from xtracter.utils.xtracter_const import VAMP_PLUGIN_BLACKLIST


class VampyPluginProvider(object):
    def __init__(self, vamp_lib=vamp):
        self.__vamp = vamp_lib

    def get_all_plugins(self):
        plugins_list = map(lambda key: self._build_analyzer(key) if not self._is_blacklisted(key) else None,
                           self.__vamp.list_plugins())
        return [plugin for plugin in plugins_list if plugin]

    def get_plugin_by_key(self, key):
        if self._analyzer_exists(key) and not self._is_blacklisted(key):
            return self._build_analyzer(key)
        raise IOError("Vamp analyzer with key {} has not been found!".format(key))

    def get_plugins_by_category(self, category):
        analyzers_available = self.get_all_plugins()
        return [analyzer for analyzer in analyzers_available if analyzer.category == category]

    def _build_analyzer(self, key):
        return VampyPlugin(key, self.__vamp.get_outputs_of(key), self.__vamp.get_category_of(key))

    def _analyzer_exists(self, key):
        return key in self.__vamp.list_plugins() and not self._is_blacklisted(key)

    def _is_blacklisted(self, key):
        return key in VAMP_PLUGIN_BLACKLIST
