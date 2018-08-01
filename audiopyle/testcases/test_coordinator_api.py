from unittest import TestCase
from assertpy import assert_that

import requests

from testcases.utils import get_api_host, get_api_port


class CoordinatorApiTest(TestCase):
    def setUp(self):
        self.coordinator_url = "http://{}:{}/".format(get_api_host(), get_api_port())

    def test_should_return_ok_after_boot(self):
        expected_status_code = 200
        expected_response = {'status': 'ok'}
        response = requests.get(url=self.coordinator_url)
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.json()).is_equal_to(expected_response)
