import unittest

import json
from assertpy import assert_that

from commons.models.plugin import VampyPlugin


class AudioPluginModelTest(unittest.TestCase):
    def setUp(self):
        self.test_plugin_provider = "test_plugin_provider"
        self.test_plugin_name = "test_plugin_name"
        self.vampy_plugin = VampyPlugin(key=("{}:{}".format(self.test_plugin_provider, self.test_plugin_name)),
                                        categories=["category1", "category2"], outputs=["output1", "output2"],
                                        library_path="/some/path")
        self.byte_symbol = "B"

    def test_model_properties(self):
        assert_that(self.vampy_plugin.name).is_equal_to(self.test_plugin_name)
        assert_that(self.vampy_plugin.provider).is_equal_to(self.test_plugin_provider)

    def test_should_serialize_and_deserialize_plugin(self):
        serialized = self.vampy_plugin.serialize()
        assert_that(serialized).is_not_none().is_not_empty()
        from_serialized = VampyPlugin.deserialize(serialized)

        assert_that(from_serialized).is_not_none().is_equal_to(self.vampy_plugin)

    def test_should_serialize_plugin_to_json(self):
        plugin_as_json = json.dumps(self.vampy_plugin.serialize())
        assert_that(plugin_as_json).is_not_none().is_not_empty()

    def test_should_have_size_defined(self):
        size_bytes = self.vampy_plugin.size_bytes()
        assert_that(size_bytes).is_between(1, 10000)

        size_bytes_humanized = self.vampy_plugin.size_humanized()
        assert_that(size_bytes_humanized).is_not_none().is_not_empty().contains(self.byte_symbol)
