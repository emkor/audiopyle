import unittest

import json
from assertpy import assert_that

from commons.models.plugin import VampyPlugin, VampyPluginParams


class AudioPluginModelTest(unittest.TestCase):
    def setUp(self):
        self.test_plugin_provider = "test_plugin_provider"
        self.test_plugin_name = "test_plugin_name"
        self.test_plugin_output = "output1"
        self.vampy_plugin = VampyPlugin(vendor=self.test_plugin_provider, name=self.test_plugin_name,
                                        output=self.test_plugin_output, library_file_name="some_lib.so")
        self.byte_symbol = "B"

    def test_model_properties(self):
        assert_that(self.vampy_plugin.name).is_equal_to(self.test_plugin_name)
        assert_that(self.vampy_plugin.vendor).is_equal_to(self.test_plugin_provider)

    def test_should_serialize_and_deserialize_plugin(self):
        serialized = self.vampy_plugin.to_serializable()
        assert_that(serialized).is_not_none().is_not_empty()
        from_serialized = VampyPlugin.from_serializable(serialized)

        assert_that(from_serialized).is_not_none().is_equal_to(self.vampy_plugin)

    def test_should_serialize_plugin_to_json(self):
        plugin_as_json = json.dumps(self.vampy_plugin.to_serializable())
        assert_that(plugin_as_json).is_not_none().is_not_empty()

    def test_should_have_size_defined(self):
        size_bytes = self.vampy_plugin.size_bytes()
        assert_that(size_bytes).is_between(1, 10000)

        size_bytes_humanized = self.vampy_plugin.size_humanized()
        assert_that(size_bytes_humanized).is_not_none().is_not_empty().contains(self.byte_symbol)


class VampyPluginConfigTest(unittest.TestCase):
    def setUp(self):
        self.empty_config = VampyPluginParams(None, None)
        self.basic_config = VampyPluginParams(2048, 4096)
        self.extended_config = VampyPluginParams(2048, 2048, sub_bands=9)

    def test_should_create_parameters_from_config(self):
        assert_that(self.empty_config.to_serializable()).is_equal_to({})
        assert_that(self.basic_config.to_serializable()).is_equal_to({"step_size": 4096, "block_size": 2048})
        assert_that(self.extended_config.to_serializable()).is_equal_to(
            {"step_size": 2048, "block_size": 2048, "sub_bands": 9})

    def test_should_serialize_and_deserialize(self):
        serialized = self.extended_config.to_serializable()
        json_serialized = json.dumps(serialized)
        assert_that(json_serialized).is_not_empty()

        deserialized = json.loads(json_serialized)
        back_to_object = VampyPluginParams.from_serializable(deserialized)
        assert_that(back_to_object).is_equal_to(self.extended_config)
