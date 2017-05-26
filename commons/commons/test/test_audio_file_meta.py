import unittest
from assertpy import assert_that

from commons.audio.segment_providing import read_audio_file_meta
from commons.test.utils import get_absolute_path_for_project_file, TEST_AUDIO_FILE


class AudioFileMetaTest(unittest.TestCase):
    def setUp(self):
        self.audio_file_name = get_absolute_path_for_project_file(__file__, TEST_AUDIO_FILE)
        self.non_existing_file_name = "/dev/21343983908329089832"

    def test_should_create_audio_file_meta(self):
        audio_file_meta = read_audio_file_meta(self.audio_file_name)
        assert_that(audio_file_meta).is_not_none()
        assert_that(audio_file_meta.bit_depth).is_equal_to(16)
        assert_that(audio_file_meta.channels_count).is_equal_to(1)
        assert_that(audio_file_meta.frames_count).is_equal_to(103936)
        assert_that(audio_file_meta.sample_rate).is_equal_to(44100)
        assert_that(audio_file_meta.file_name).is_equal_to('102bpm_drum_loop_mono_44.1k.wav')
        assert_that(audio_file_meta.absolute_path).is_equal_to(self.audio_file_name)

    def test_should_return_none_on_non_existing_file(self):
        audio_file_meta = read_audio_file_meta(self.non_existing_file_name)
        assert_that(audio_file_meta).is_none()
