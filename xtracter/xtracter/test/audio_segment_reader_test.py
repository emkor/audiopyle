import unittest
from mock import Mock

from assertpy import assert_that

from xtracter.model.audio_segment import AudioSegment
from xtracter.service.audio_segment_reader import AudioSegmentReader
from xtracter.utils.xtracter_utils import XtracterUtils


class AudioSegmentReaderIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.segment_reader = AudioSegmentReader(Mock())

    def test_should_resize_and_fill_with(self):
        segment = AudioSegment(XtracterUtils.import_test_file_csv_data(), 44100)
        desired_size = 110000
        fill = 0.0
        resized_segment = self.segment_reader._resize_and_fill_with(segment, block_size=desired_size, fill=fill)
        assert_that(resized_segment.length_frames()).is_equal_to(desired_size)
        assert_that(resized_segment.data[-1]).is_equal_to(fill)
        assert_that(resized_segment.data[-2]).is_equal_to(fill)
