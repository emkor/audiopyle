from unittest import TestCase
from assertpy import assert_that

from testcases.utils import keep_polling_until


class CoordinatorApiTest(TestCase):
    def setUp(self):
        self.coordinator_url = "http://coordinator1:8080/"
        self.timeout = 5.

    def test_should_return_ok_after_boot(self):
        response = keep_polling_until(url=self.coordinator_url, expected_status=200, timeout=self.timeout)
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()).is_equal_to("nok")
