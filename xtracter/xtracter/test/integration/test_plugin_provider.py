import unittest

from assertpy import assert_that

from commons.model.vampy_plugin import VampyPlugin
from xtracter.provider.plugin_provider import VampyPluginProvider


class VampyPluginProviderIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.plugin_provider = VampyPluginProvider()

    def test_any_plugin_in_system(self):
        plugins = self.plugin_provider.get_all_plugins()
        assert_that(plugins).is_not_none().is_not_empty()
        assert_that(isinstance(plugins[0], VampyPlugin)).is_true()
