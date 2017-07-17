from unittest import TestCase
from assertpy import assert_that

import requests

from commons.vampy.plugin import VampyPlugin
from testcases.utils import get_service_host_name


class PluginApiTest(TestCase):
    def setUp(self):
        self.plugin_url = "http://{}:8080/plugin".format(get_service_host_name("coordinator"))

    def test_should_return_ok_after_boot(self):
        expected_status_code = 200
        expected_plugin_count = 6
        expected_first_plugin = VampyPlugin(key="vamp-example-plugins:amplitudefollower",
                                            categories=["Low Level Features"],
                                            outputs=["amplitude"],
                                            library_path="/root/vamp/vamp-example-plugins.so")
        response = requests.get(url=self.plugin_url)
        assert_that(response.status_code).is_equal_to(expected_status_code)
        actual_response = response.json()
        assert_that(actual_response).is_length(expected_plugin_count)
        assert_that(actual_response).contains(expected_first_plugin.serialize())
