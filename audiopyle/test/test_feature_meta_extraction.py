import unittest

import numpy
from assertpy import assert_that

from audiopyle.commons.services.metric_provider import _extract_data_stats


class FeatureMetaExtractionTest(unittest.TestCase):
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
        assert_that(data_stats.maximum).is_not_none().is_equal_to(3.0)
        assert_that(data_stats.minimum).is_not_none().is_equal_to(0.0)
        assert_that(data_stats.mean).is_not_none().is_equal_to(1.5)
        assert_that(data_stats.median).is_not_none().is_equal_to(1.5)
        assert_that(data_stats.standard_deviation).is_not_none().is_between(0.95, 0.96)
        assert_that(data_stats.variance).is_not_none().is_between(0.91, 0.92)

    def test_should_calculate_stats_on_square_matrix(self):
        data_stats = _extract_data_stats(self.np_square_matrix)
        assert_that(data_stats).is_not_none()
        assert_that(data_stats.maximum).is_not_none().is_equal_to(3.0)
        assert_that(data_stats.minimum).is_not_none().is_equal_to(0.0)
        assert_that(data_stats.mean).is_not_none().is_between(1.6, 1.7)
        assert_that(data_stats.median).is_not_none().is_equal_to(2.0)
        assert_that(data_stats.standard_deviation).is_not_none().is_between(0.94, 0.95)
        assert_that(data_stats.variance).is_not_none().is_between(0.88, 0.89)

    def test_should_calculate_stats_on_non_square_matrix(self):
        data_stats = _extract_data_stats(self.np_non_square_matrix)
        assert_that(data_stats).is_not_none()
        assert_that(data_stats.maximum).is_not_none().is_equal_to(3.0)
        assert_that(data_stats.minimum).is_not_none().is_equal_to(0.0)
        assert_that(data_stats.mean).is_not_none().is_equal_to(1.5)
        assert_that(data_stats.median).is_not_none().is_equal_to(1.5)
        assert_that(data_stats.standard_deviation).is_not_none().is_between(0.95, 0.96)
        assert_that(data_stats.variance).is_not_none().is_between(0.91, 0.92)
