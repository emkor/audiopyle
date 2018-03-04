from unittest import TestCase

import requests
from assertpy import assert_that

from commons.models.plugin import VampyPlugin
from testcases.utils import get_api_host


class PluginApiTest(TestCase):
    def setUp(self):
        self.plugin_url = "http://{}:8080/plugin".format(get_api_host())

    def test_should_list_plugins(self):
        expected_status_code = 200
        expected_plugin_count = 6
        expected_first_plugin = VampyPlugin(key="vamp-example-plugins:amplitudefollower",
                                            categories=["Low Level Features"],
                                            outputs=["amplitude"],
                                            library_file_name="vamp-example-plugins.so")
        response = requests.get(url=self.plugin_url)
        assert_that(response.status_code).is_equal_to(expected_status_code)
        actual_response = response.json()
        assert_that(actual_response).is_length(expected_plugin_count)
        assert_that(actual_response).contains(expected_first_plugin.to_serializable())
