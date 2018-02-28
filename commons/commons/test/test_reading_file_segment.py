import unittest

from assertpy import assert_that

from commons.services.file_meta_providing import read_mp3_file_meta
from commons.services.segment_providing import read_raw_audio_from_mp3
from commons.test.utils import get_absolute_path_for_project_file, TEST_MP3_AUDIO_FILE


class TestReadingRawAudio(unittest.TestCase):
    def setUp(self):
        self.mp3_file_meta = read_mp3_file_meta(get_absolute_path_for_project_file(__file__, TEST_MP3_AUDIO_FILE))

    def test_read_mp3_data_should_have_correct_length_and_value_range(self):
        mp3_raw_data = read_raw_audio_from_mp3(self.mp3_file_meta.absolute_path)
        assert_that(len(mp3_raw_data))\
            .is_less_than_or_equal_to(105984)\
            .is_greater_than_or_equal_to(104879)  # on CI PyDub is returning higher number of frames - dunno why
        assert_that(mp3_raw_data.max()).is_less_than_or_equal_to(1.).is_greater_than(0.5)
        assert_that(mp3_raw_data.min()).is_greater_than_or_equal_to(-1.).is_less_than(-0.5)
