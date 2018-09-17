import unittest

from assertpy import assert_that

from audiopyle.lib.services.audio_providing import read_raw_audio_from_file
from audiopyle.test.utils import get_absolute_path_for_project_file, TEST_MP3_AUDIO_FILE


class AudioNormalizationTest(unittest.TestCase):
    def setUp(self):
        self.mp3_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_MP3_AUDIO_FILE)

    def test_should_normalize_volume_in_mp3_file(self):
        raw_audio = read_raw_audio_from_file(self.mp3_audio_file_name)
        assert_that((1. >= max(raw_audio) >= 0.999) or (-1. <= min(raw_audio) <= -0.999)).is_true()
