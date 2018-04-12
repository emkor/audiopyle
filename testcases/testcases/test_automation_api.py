from unittest import TestCase
from assertpy import assert_that

import requests

from commons.abstractions.api_model import HttpStatusCode
from testcases.utils import get_api_host, get_api_port


class AutomationApiTest(TestCase):
    def setUp(self):
        self.automation_api_url = "http://{}:{}/automation".format(get_api_host(), get_api_port())

    def test_should_return_method_not_allowed_on_get(self):
        response = requests.get(self.automation_api_url)
        assert_that(response.status_code).is_equal_to(HttpStatusCode.method_not_allowed.value)
