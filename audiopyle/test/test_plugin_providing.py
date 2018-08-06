import unittest
from typing import List, Dict

from assertpy import assert_that

from audiopyle.commons.models.plugin import VampyPlugin
from audiopyle.commons.services.plugin_providing import VampyPluginProvider


class TestPluginProviding(unittest.TestCase):
    def setUp(self):
        self.plugin_key_to_outputs = {
            "test_plugin_vendor:test_plugin_name": ["output1", "output2"],
            "test_plugin_vendor_2:test_plugin_name_2": ["output1", "output2", "output3"]
        }
        self.plugin_key_to_lib_file = {
            "test_plugin_vendor:test_plugin_name": "plugin_lib.so",
            "test_plugin_vendor_2:test_plugin_name_2": "plugin_lib_2.so"
        }
        self.vampy_plugin_1 = VampyPlugin(vendor="test_plugin_vendor", name="test_plugin_name",
                                          output="output1", library_file_name="plugin_lib.so")
        self.vampy_plugin_2 = VampyPlugin(vendor="test_plugin_vendor", name="test_plugin_name",
                                          output="output2", library_file_name="plugin_lib.so")
        self.vampy_plugin_3 = VampyPlugin(vendor="test_plugin_vendor_2", name="test_plugin_name_2",
                                          output="output1", library_file_name="plugin_lib_2.so")
        self.vampy_plugin_4 = VampyPlugin(vendor="test_plugin_vendor_2", name="test_plugin_name_2",
                                          output="output2", library_file_name="plugin_lib_2.so")
        self.vampy_plugin_5 = VampyPlugin(vendor="test_plugin_vendor_2", name="test_plugin_name_2",
                                          output="output3", library_file_name="plugin_lib_2.so")
        self.vamp_interface_mock = VampInterfaceStub(self.plugin_key_to_outputs)
        self.vamp_host_interface_mock = VampHostInterfaceStub(self.plugin_key_to_lib_file)

    def _set_up_plugin_provider(self, blacklist: List[str]):
        return VampyPluginProvider(self.vamp_interface_mock, self.vamp_host_interface_mock, blacklist)

    def test_should_return_all_plugins_when_black_list_is_empty(self):
        plugin_provider = self._set_up_plugin_provider([])
        full_plugin_keys = plugin_provider.list_full_plugin_keys()
        assert_that(full_plugin_keys).is_length(5).contains(
            "test_plugin_vendor:test_plugin_name:output1",
            "test_plugin_vendor:test_plugin_name:output2",
            "test_plugin_vendor_2:test_plugin_name_2:output1",
            "test_plugin_vendor_2:test_plugin_name_2:output2",
            "test_plugin_vendor_2:test_plugin_name_2:output3"
        )
        vampy_plugins = plugin_provider.list_vampy_plugins()
        assert_that(vampy_plugins).is_length(5).contains(self.vampy_plugin_1, self.vampy_plugin_2, self.vampy_plugin_3,
                                                         self.vampy_plugin_4, self.vampy_plugin_5)

    def test_should_omit_certain_blacklisted_plugins(self):
        plugin_provider = self._set_up_plugin_provider(["test_plugin_vendor:test_plugin_name:output2",
                                                        "test_plugin_vendor_2:test_plugin_name_2:output2"])
        full_plugin_keys = plugin_provider.list_full_plugin_keys()
        assert_that(full_plugin_keys).is_length(3).contains(
            "test_plugin_vendor:test_plugin_name:output1",
            "test_plugin_vendor_2:test_plugin_name_2:output1",
            "test_plugin_vendor_2:test_plugin_name_2:output3"
        )

        vampy_plugins = plugin_provider.list_vampy_plugins()
        assert_that(vampy_plugins).is_length(3).contains(self.vampy_plugin_1, self.vampy_plugin_3, self.vampy_plugin_5)


class VampInterfaceStub(object):
    def __init__(self, plugin_vampy_key_to_outputs: Dict[str, List[str]]) -> None:
        self.plugin_vampy_key_to_outputs = plugin_vampy_key_to_outputs

    def get_outputs_of(self, vampy_plugin_key: str) -> List[str]:
        return self.plugin_vampy_key_to_outputs[vampy_plugin_key]

    def list_plugins(self) -> List[str]:
        return list(self.plugin_vampy_key_to_outputs.keys())


class VampHostInterfaceStub(object):
    def __init__(self, plugin_vampy_key_to_lib_file_name: Dict[str, str]) -> None:
        self.plugin_vampy_key_to_lib_file_name = plugin_vampy_key_to_lib_file_name

    def get_library_for(self, vampy_key: str) -> str:
        return self.plugin_vampy_key_to_lib_file_name[vampy_key]
