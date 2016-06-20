import unittest
from numpy.testing import assert_array_equal, assert_almost_equal

from assertpy import assert_that
from numpy import array

from xtracter.provider.audio_segment_provider import LocalAudioSegmentProvider


class LocalAudioSegmentProviderTest(unittest.TestCase):
    def setUp(self):
        self.segment_provider = LocalAudioSegmentProvider(None)

    def test_split_by_channels_stereo(self):
        channels = 2
        test_data = array([1, 2, 3, 4, 5, 6, 7])
        expected_left = array([1, 3, 5, 7])
        expected_right = array([2, 4, 6])
        actual_left, actual_right = self.segment_provider._split_by_channels(test_data, channels)
        assert_array_equal(actual_left, expected_left)
        assert_array_equal(actual_right, expected_right)

    def test_split_by_channels_mono(self):
        channels = 1
        test_data = array([1, 2, 3, 4, 5, 6, 7])
        left, right = self.segment_provider._split_by_channels(test_data, channels)
        assert_array_equal(left, test_data)
        assert_that(right).is_none()

    def test_normalize(self):
        test_data = array([3276.7, 6553.4, 9830.1, 13106.8, 16383.5, 19660.2, 22936.9])
        test_data_normalized = self.segment_provider._normalize(test_data)
        assert_that(test_data_normalized).is_not_none()
        assert_almost_equal(test_data_normalized, [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], decimal=10)

    def test_normalize_channel_is_none(self):
        test_data = None
        test_data_normalized = self.segment_provider._normalize(test_data)
        assert_that(test_data_normalized).is_none()

    def test_normalize_edge_cases(self):
        test_data = array([32767, 0])
        test_data_normalized = self.segment_provider._normalize(test_data)
        assert_that(test_data_normalized).is_not_none()
        assert_almost_equal(test_data_normalized, [1.0, 0.0], decimal=10)
