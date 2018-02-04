import unittest

import numpy
from assertpy import assert_that

from commons.services.feature_extraction import _extract_data_stats


class FeatureExtractionTest(unittest.TestCase):
    def setUp(self):
        self.np_vector = numpy.asanyarray([1.0, 2.0, 3.0, 2.0, 1.0, 0.0])
        self.np_square_matrix = numpy.asanyarray([
            [1.0, 2.0, 3.0],
            [2.0, 1.0, 0.0],
            [1.0, 2.0, 3.0]
        ])
        self.np_non_square_matrix = numpy.asanyarray([
            [1.0, 2.0, 3.0],
            [2.0, 1.0, 0.0]
        ])

    def test_should_calculate_stats_on_vector(self):
        data_stats = _extract_data_stats(self.np_vector)
        assert_that(data_stats).is_not_none()

    def test_should_calculate_stats_on_square_matrix(self):
        data_stats = _extract_data_stats(self.np_square_matrix)
        assert_that(data_stats).is_not_none()

    def test_should_calculate_stats_on_non_square_matrix(self):
        data_stats = _extract_data_stats(self.np_non_square_matrix)
        assert_that(data_stats).is_not_none()
