import unittest
from mock import Mock

from assertpy import assert_that

from xtracter.provider.plugin_provider import VampyPluginProvider

PLUGIN_CAT_1 = 'cat1'
PLUGIN_CAT_2 = 'cat2'
QM_TEMPOTRACKER_PLUGIN = 'qm-vamp-plugins:qm-tempotracker'
BBC_INTENSITY_PLUGIN = 'bbc-vamp-plugins:bbc-intensity'
BBC_ENERGY_PLUGIN = 'bbc-vamp-plugins:bbc-energy'


class VampyPluginProviderTest(unittest.TestCase):
    def setUp(self):
        self.mocked_vamp_lib = self._mock_vamp_lib()
        self.plugin = VampyPluginProvider(self.mocked_vamp_lib)

    def test_should_list_all_plugins(self):
        all_plugins = self.plugin.get_all_plugins()
        all_plugin_keys = map(lambda plugin: plugin.key, all_plugins)
        assert_that(len(all_plugins)).is_equal_to(3)
        assert_that(all_plugin_keys).contains(QM_TEMPOTRACKER_PLUGIN, BBC_ENERGY_PLUGIN, BBC_INTENSITY_PLUGIN)

    def test_should_get_plugin_by_key(self):
        plugin = self.plugin.get_plugin_by_key(QM_TEMPOTRACKER_PLUGIN)
        assert_that(plugin).is_not_none()
        assert_that(plugin.key).is_equal_to(QM_TEMPOTRACKER_PLUGIN)

    def test_should_list_all_plugins_except_blacklisted(self):
        self._mock_is_blacklisted([BBC_ENERGY_PLUGIN])
        all_plugins = self.plugin.get_all_plugins()
        all_plugin_keys = map(lambda plugin: plugin.key, all_plugins)
        assert_that(len(all_plugins)).is_equal_to(2)
        assert_that(all_plugin_keys).contains(QM_TEMPOTRACKER_PLUGIN, BBC_INTENSITY_PLUGIN)

    def test_get_plugins_by_category(self):
        plugins = self.plugin.get_plugins_by_category(PLUGIN_CAT_2)
        plugin_keys = map(lambda plugin: plugin.key, plugins)
        assert_that(len(plugins)).is_equal_to(2)
        assert_that(plugin_keys).contains(BBC_ENERGY_PLUGIN, BBC_INTENSITY_PLUGIN)

    def _mock_vamp_lib(self):
        vamp_mock = Mock()
        vamp_mock.list_plugins.return_value = [QM_TEMPOTRACKER_PLUGIN, BBC_INTENSITY_PLUGIN, BBC_ENERGY_PLUGIN]
        vamp_mock.get_category_of.side_effect = self._mock_vamp_lib_get_category
        vamp_mock.get_outputs_of.side_effect = self._mock_vamp_lib_get_outputs
        return vamp_mock

    def _mock_vamp_lib_get_category(self, plugin):
        return PLUGIN_CAT_1 if plugin == QM_TEMPOTRACKER_PLUGIN else PLUGIN_CAT_2

    def _mock_vamp_lib_get_outputs(self, plugin):
        return ['time'] if plugin == QM_TEMPOTRACKER_PLUGIN else ['smthng1']

    def _mock_is_blacklisted(self, blacklist):
        def _is_blacklisted(key):
            return key in blacklist

        self.plugin._is_blacklisted = Mock(side_effect=_is_blacklisted)
