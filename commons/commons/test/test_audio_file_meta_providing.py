import unittest
from datetime import datetime

from assertpy import assert_that

from commons.services.file_meta_providing import read_wav_file_meta, read_mp3_file_meta, read_file_meta
from commons.test.utils import get_absolute_path_for_project_file, TEST_WAV_AUDIO_FILE, TEST_MP3_AUDIO_FILE


class FileMetaProvidingTest(unittest.TestCase):
    def setUp(self):
        self.wav_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_WAV_AUDIO_FILE)
        self.non_existing_file_name = "/dev/21343983908329089832"

    def test_should_return_file_meta_from_wav(self):
        file_meta = read_file_meta(self.wav_audio_file_name)
        assert_that(file_meta).is_not_none()
        assert_that(file_meta.extension).is_equal_to("wav")
        assert_that(file_meta.file_name).is_equal_to("102bpm_drum_loop_mono_44.1k.wav")
        assert_that(file_meta.size).is_equal_to(207916)
        assert_that(file_meta.created_on).is_not_none().is_after(datetime(year=2017, month=1, day=1))
        assert_that(file_meta.last_access).is_not_none().is_after(datetime(year=2017, month=10, day=1))
        assert_that(file_meta.last_modification).is_not_none().is_after(datetime(year=2017, month=3, day=1))

    def test_should_return_none_on_non_existing_file(self):
        file_meta = read_file_meta(self.non_existing_file_name)
        assert_that(file_meta).is_none()


class WavAudioFileMetaProvidingTest(unittest.TestCase):
    def setUp(self):
        self.wav_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_WAV_AUDIO_FILE)
        self.wav_audio_file_sample_rate = 44100
        self.wav_audio_file_length_seconds = 2.357
        self.wav_audio_file_bit_rate_kbps = 705.1
        self.wav_audio_file_frame_count = 103936
        self.non_existing_file_name = "/dev/21343983908329089832"

    def test_should_create_wav_audio_file_meta(self):
        wav_audio_file_meta = read_wav_file_meta(self.wav_audio_file_name)
        assert_that(wav_audio_file_meta).is_not_none()
        assert_that(wav_audio_file_meta.bit_depth).is_equal_to(16)
        assert_that(wav_audio_file_meta.channels_count).is_equal_to(1)
        assert_that(wav_audio_file_meta.frames_count).is_equal_to(self.wav_audio_file_frame_count)
        assert_that(wav_audio_file_meta.sample_rate).is_equal_to(self.wav_audio_file_sample_rate)
        assert_that(wav_audio_file_meta.bit_rate_kbps).is_equal_to(self.wav_audio_file_bit_rate_kbps)
        assert_that(wav_audio_file_meta.length_sec).is_equal_to(self.wav_audio_file_length_seconds)

    def test_should_return_none_on_non_existing_file(self):
        wav_audio_file_meta = read_wav_file_meta(self.non_existing_file_name)
        assert_that(wav_audio_file_meta).is_none()


class Mp3AudioFileMetaProvidingTest(unittest.TestCase):
    def setUp(self):
        self.mp3_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_MP3_AUDIO_FILE)
        self.mp3_audio_file_sample_rate = 44100
        self.mp3_audio_file_length_seconds = 2.403
        self.mp3_audio_file_bit_rate_kbps_between = 127.0, 130.0
        self.non_existing_file_name = "/dev/21343983908329089832"

    def test_should_create_mp3_audio_file_meta(self):
        mp3_audio_file_meta = read_mp3_file_meta(self.mp3_audio_file_name)
        assert_that(mp3_audio_file_meta).is_not_none()
        assert_that(mp3_audio_file_meta.channels_count).is_equal_to(1)
        assert_that(mp3_audio_file_meta.sample_rate).is_equal_to(self.mp3_audio_file_sample_rate)
        assert_that(mp3_audio_file_meta.bit_rate_kbps).is_between(self.mp3_audio_file_bit_rate_kbps_between[0],
                                                                  self.mp3_audio_file_bit_rate_kbps_between[1])
        assert_that(mp3_audio_file_meta.length_sec).is_equal_to(self.mp3_audio_file_length_seconds)

    def test_should_return_none_on_non_existing_file(self):
        mp3_audio_file_meta = read_mp3_file_meta(self.non_existing_file_name)
        assert_that(mp3_audio_file_meta).is_none()
