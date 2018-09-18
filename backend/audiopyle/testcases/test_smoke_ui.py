from unittest import TestCase
from assertpy import assert_that

import requests

from audiopyle.testcases.utils import get_ui_port, get_ui_host


class UiSmokeTest(TestCase):
    def setUp(self):
        self.ui_url = "http://{}:{}/".format(get_ui_host(), get_ui_port())

    def test_should_return_ok_on_ui(self):
        expected_status_code = 200
        response = requests.get(url=self.ui_url)
        assert_that(response.status_code).is_equal_to(expected_status_code)
        assert_that(response.content).is_not_empty()
