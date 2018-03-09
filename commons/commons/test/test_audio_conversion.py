import unittest
from datetime import datetime, timedelta

from assertpy import assert_that

from commons.utils.conversion import seconds_between


class ConversionUtilsTest(unittest.TestCase):
    def test_should_measure_seconds_since_event(self):
        start_point = datetime.utcnow() - timedelta(seconds=1.5)
        time_that_passed = seconds_between(start_point)
        assert_that(time_that_passed).is_between(1.5, 2.0)

    def test_should_measure_seconds_between_events(self):
        end_point = datetime.utcnow()
        start_point = end_point - timedelta(seconds=2.5)
        time_that_passed = seconds_between(start_point, end_point)
        assert_that(time_that_passed).is_between(2.499, 2.501)
