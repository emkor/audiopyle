from unittest import TestCase

import requests
from assertpy import assert_that

from audiopyle.testcases.utils import get_api_host, get_api_port


class ConfigApiTest(TestCase):
    def setUp(self):
        self.plugin_config_url = "http://{}:{}/config/plugin".format(get_api_host(), get_api_port())
        self.metric_config_url = "http://{}:{}/config/metric".format(get_api_host(), get_api_port())

    def test_should_return_plugin_config_content(self):
        expected_status_code = 200
        expected_plugin_config_records_count = 1
        response = requests.get(url=self.plugin_config_url)

        assert_that(response.status_code).is_equal_to(expected_status_code)
        json_response = response.json()
        assert_that(len(json_response.keys())).is_greater_than_or_equal_to(expected_plugin_config_records_count)

    def test_should_return_metric_config_content(self):
        expected_status_code = 200
        expected_metric_config_records_count = 3
        response = requests.get(url=self.metric_config_url)

        assert_that(response.status_code).is_equal_to(expected_status_code)
        json_response = response.json()
        assert_that(len(json_response.keys())).is_greater_than_or_equal_to(expected_metric_config_records_count)
