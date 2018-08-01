import unittest
from datetime import datetime

from assertpy import assert_that

from audiopyle.commons.services.file_meta_providing import read_audio_file_meta, read_file_meta
from audiopyle.test.utils import get_absolute_path_for_project_file, TEST_MP3_AUDIO_FILE, TEST_FLAC_AUDIO_FILE
from audiopyle.commons.utils.file_system import get_file_name


class FileMetaProvidingTest(unittest.TestCase):
    def setUp(self):
        self.mp3_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_MP3_AUDIO_FILE)
        self.flac_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_FLAC_AUDIO_FILE)
        self.non_existing_file_name = "/dev/21343983908329089832"

    def test_should_return_file_meta_from_mp3(self):
        file_meta = read_file_meta(self.mp3_audio_file_name)
        assert_that(file_meta).is_not_none()
        assert_that(file_meta.extension).is_equal_to("mp3")
        assert_that(file_meta.file_name).is_equal_to("102bpm_drum_loop.mp3")
        assert_that(file_meta.created_on).is_not_none().is_after(datetime(year=2017, month=1, day=1))
        assert_that(file_meta.last_access).is_not_none().is_after(datetime(year=2017, month=10, day=1))
        assert_that(file_meta.last_modification).is_not_none().is_after(datetime(year=2017, month=3, day=1))

    def test_should_return_file_meta_from_flac(self):
        file_meta = read_file_meta(self.flac_audio_file_name)
        assert_that(file_meta).is_not_none()
        assert_that(file_meta.extension).is_equal_to("flac")
        assert_that(file_meta.file_name).is_equal_to("102bpm_drum_loop.flac")
        assert_that(file_meta.created_on).is_not_none().is_after(datetime(year=2018, month=7, day=7))
        assert_that(file_meta.last_access).is_not_none().is_after(datetime(year=2017, month=7, day=9))
        assert_that(file_meta.last_modification).is_not_none().is_after(datetime(year=2017, month=7, day=8))

    def test_should_return_none_on_non_existing_file(self):
        file_meta = read_file_meta(self.non_existing_file_name)
        assert_that(file_meta).is_none()


class AudioFileMetaProvidingTest(unittest.TestCase):
    def setUp(self):
        self.non_existing_file_name = "/dev/21343983908329089832"
        self.mp3_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_MP3_AUDIO_FILE)
        self.flac_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_FLAC_AUDIO_FILE)
        self.audio_file_sample_rate = 44100
        self.audio_file_length_seconds_between = (2.36, 2.41)
        self.mp3_audio_file_bit_rate_kbps_between = (127.0, 130.0)
        self.flac_audio_file_bit_rate_kbps_between = (350.0, 400.0)

    def test_should_create_mp3_audio_file_meta(self):
        mp3_audio_file_meta = read_audio_file_meta(self.mp3_audio_file_name)
        assert_that(mp3_audio_file_meta).is_not_none()
        assert_that(mp3_audio_file_meta.channels_count).is_equal_to(1)
        assert_that(mp3_audio_file_meta.sample_rate).is_equal_to(self.audio_file_sample_rate)
        assert_that(mp3_audio_file_meta.file_name).is_equal_to(get_file_name(TEST_MP3_AUDIO_FILE))
        assert_that(mp3_audio_file_meta.bit_rate_kbps).is_between(*self.mp3_audio_file_bit_rate_kbps_between)
        assert_that(mp3_audio_file_meta.length_sec).is_between(*self.audio_file_length_seconds_between)

    def test_should_create_flac_audio_file_meta(self):
        flac_audio_file_meta = read_audio_file_meta(self.flac_audio_file_name)
        assert_that(flac_audio_file_meta).is_not_none()
        assert_that(flac_audio_file_meta.channels_count).is_equal_to(1)
        assert_that(flac_audio_file_meta.sample_rate).is_equal_to(self.audio_file_sample_rate)
        assert_that(flac_audio_file_meta.file_name).is_equal_to(get_file_name(TEST_FLAC_AUDIO_FILE))
        assert_that(flac_audio_file_meta.bit_rate_kbps).is_between(*self.flac_audio_file_bit_rate_kbps_between)
        assert_that(flac_audio_file_meta.length_sec).is_between(*self.audio_file_length_seconds_between)

    def test_should_return_none_on_non_existing_file(self):
        mp3_audio_file_meta = read_audio_file_meta(self.non_existing_file_name)
        assert_that(mp3_audio_file_meta).is_none()
