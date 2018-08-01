from unittest import TestCase

import requests
from assertpy import assert_that

from audiopyle.commons.models.plugin import VampyPlugin
from audiopyle.testcases.utils import get_api_host, get_api_port


class PluginApiTest(TestCase):
    def setUp(self):
        self.plugin_url = "http://{}:{}/plugin".format(get_api_host(), get_api_port())
        self.test_plugin_vendor = "vamp-example-plugins"
        self.test_plugin_name = "amplitudefollower"
        self.test_plugin_output = "amplitude"
        self.test_plugin_lib_name = "vamp-example-plugins.so"
        self.test_plugin = VampyPlugin(vendor=self.test_plugin_vendor, name=self.test_plugin_name,
                                       output=self.test_plugin_output, library_file_name=self.test_plugin_lib_name)

    def test_should_list_plugins(self):
        expected_status_code = 200
        expected_plugin_count = 6
        response = requests.get(url=self.plugin_url)
        assert_that(response.status_code).is_equal_to(expected_status_code)
        actual_response = response.json()
        assert_that(actual_response).is_length(expected_plugin_count)

    def test_should_read_plugin_details(self):
        expected_status_code = 200
        expected_plugin = VampyPlugin(vendor="vamp-example-plugins",
                                      name="amplitudefollower",
                                      output="amplitude",
                                      library_file_name="vamp-example-plugins.so")
        response = requests.get(url="{}/{}/{}/{}".format(self.plugin_url, self.test_plugin_vendor,
                                                         self.test_plugin_name, self.test_plugin_output))
        assert_that(response.status_code).is_equal_to(expected_status_code)
        actual_plugin = VampyPlugin.from_serializable(response.json())
        assert_that(actual_plugin).is_equal_to(expected_plugin)
