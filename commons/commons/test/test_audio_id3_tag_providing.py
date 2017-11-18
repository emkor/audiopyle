import unittest

from assertpy import assert_that

from commons.audio.audio_tag import Id3Tag
from commons.services.audio_tag_providing import read_id3_tag
from commons.test.utils import get_absolute_path_for_project_file, TEST_MP3_AUDIO_FILE, TEST_WAV_AUDIO_FILE


class AudioFileId3TagProvidingTest(unittest.TestCase):
    def setUp(self):
        self.wav_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_WAV_AUDIO_FILE)
        self.mp3_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_MP3_AUDIO_FILE)
        self.non_existing_file_path = "/tmp/non-existing-file-0"
        self.mp3_file_id3_tag = Id3Tag(artist="Unknown Artist", title="Unknown Title", album="Unknown Album",
                                       date=2017, track=1, genre="Unknown Genre")

    def test_should_read_id3_tag(self):
        id3_tag_from_mp3 = read_id3_tag(self.mp3_audio_file_name)
        assert_that(id3_tag_from_mp3).is_equal_to(self.mp3_file_id3_tag)

    def test_should_return_none_on_wav_file(self):
        id3_tag_from_wav = read_id3_tag(self.wav_audio_file_name)
        assert_that(id3_tag_from_wav).is_none()

    def test_should_return_none_on_non_existing_file(self):
        assert_that(read_id3_tag).raises(IOError).when_called_with(self.non_existing_file_path)
