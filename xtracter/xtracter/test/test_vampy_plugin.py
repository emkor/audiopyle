import unittest

from assertpy import assert_that

from commons.model.vampy_plugin import VampyPlugin


class VampyPluginTest(unittest.TestCase):
    plugin_1 = VampyPlugin("bbc-vamp-plugins:bbc-rhythm", ["tempo", "energy"], "time")
    plugin_2 = VampyPlugin("nnls-chroma:nnls-chroma", ["matrix"], "time")

    def test_get_provider(self):
        plugin_1_expected_provider = "bbc-vamp-plugins"
        plugin_1_actual_provider = self.plugin_1.get_provider()

        plugin_2_expected_provider = "nnls-chroma"
        plugin_2_actual_provider = self.plugin_2.get_provider()

        assert_that(plugin_1_actual_provider).is_equal_to(plugin_1_expected_provider)
        assert_that(plugin_2_actual_provider).is_equal_to(plugin_2_expected_provider)

    def test_get_name(self):
        plugin_1_expected_name = "bbc-rhythm"
        plugin_1_actual_name = self.plugin_1.get_name()

        plugin_2_expected_name = "nnls-chroma"
        plugin_2_actual_name = self.plugin_2.get_name()

        assert_that(plugin_1_actual_name).is_equal_to(plugin_1_expected_name)
        assert_that(plugin_2_actual_name).is_equal_to(plugin_2_expected_name)

    def test_get_outputs(self):
        plugin_1_expected_outputs = {"energy", "tempo"}
        plugin_1_actual_outputs = set(self.plugin_1.outputs)

        plugin_2_expected_outputs = {"matrix"}
        plugin_2_actual_outputs = set(self.plugin_2.outputs)

        assert_that(plugin_1_actual_outputs).is_equal_to(plugin_1_expected_outputs)
        assert_that(plugin_2_actual_outputs).is_equal_to(plugin_2_expected_outputs)
