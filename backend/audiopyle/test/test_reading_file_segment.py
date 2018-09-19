import unittest

from assertpy import assert_that

from audiopyle.lib.services.audio_providing import read_raw_audio_from_file
from audiopyle.test.utils import get_absolute_path_for_project_file, TEST_MP3_AUDIO_FILE, TEST_FLAC_AUDIO_FILE


class TestReadingRawAudio(unittest.TestCase):
    def setUp(self):
        self.absolute_path_to_mp3 = get_absolute_path_for_project_file(__file__, TEST_MP3_AUDIO_FILE)
        self.absolute_path_to_flac = get_absolute_path_for_project_file(__file__, TEST_FLAC_AUDIO_FILE)
        self.frames_count_between = (104879, 105984)  # on CI PyDub is returning higher number of frames - dunno why
        self.wave_min_between = (0.5, 1.)
        self.wave_max_between = (-1, -0.5)

    def test_read_mp3_data_should_have_correct_length_and_value_range(self):
        mp3_raw_data = read_raw_audio_from_file(self.absolute_path_to_mp3)
        assert_that(len(mp3_raw_data)).is_between(self.frames_count_between[0],
                                                  self.frames_count_between[1])
        assert_that(mp3_raw_data.max()).is_between(*self.wave_min_between)
        assert_that(mp3_raw_data.min()).is_between(*self.wave_max_between)

    def test_read_flac_data_should_have_correct_length_and_value_range(self):
        flac_raw_data = read_raw_audio_from_file(self.absolute_path_to_flac)
        assert_that(len(flac_raw_data)).is_between(self.frames_count_between[0],
                                                   self.frames_count_between[1])
        assert_that(flac_raw_data.max()).is_between(*self.wave_min_between)
        assert_that(flac_raw_data.min()).is_between(*self.wave_max_between)
