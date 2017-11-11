import unittest

from assertpy import assert_that

from commons.audio.file_meta_providing import read_wav_file_meta
from commons.test.utils import get_absolute_path_for_project_file, TEST_WAV_AUDIO_FILE


class AudioFileMetaProvidingTest(unittest.TestCase):
    def setUp(self):
        self.audio_file_name = get_absolute_path_for_project_file(__file__, TEST_WAV_AUDIO_FILE)
        self.non_existing_file_name = "/dev/21343983908329089832"

    def test_should_create_audio_file_meta(self):
        audio_file_meta = read_wav_file_meta(self.audio_file_name)
        assert_that(audio_file_meta).is_not_none()
        assert_that(audio_file_meta.bit_depth).is_equal_to(16)
        assert_that(audio_file_meta.channels_count).is_equal_to(1)
        assert_that(audio_file_meta.frames_count).is_equal_to(103936)
        assert_that(audio_file_meta.sample_rate).is_equal_to(44100)
        assert_that(audio_file_meta.absolute_path).is_equal_to(self.audio_file_name)

    def test_should_return_none_on_non_existing_file(self):
        audio_file_meta = read_wav_file_meta(self.non_existing_file_name)
        assert_that(audio_file_meta).is_none()
