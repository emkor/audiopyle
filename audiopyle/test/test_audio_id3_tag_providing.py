import unittest

from assertpy import assert_that
from mutagen.id3 import ID3NoHeaderError

from audiopyle.lib.models.audio_tag import Id3Tag
from audiopyle.lib.services.audio_tag_providing import read_audio_tag_using, read_audio_tag
from audiopyle.test.utils import get_absolute_path_for_project_file, TEST_MP3_AUDIO_FILE, TEST_FLAC_AUDIO_FILE


def function_raising_error(*args, **kwargs):
    raise ID3NoHeaderError()


class AudioFileId3TagProvidingTest(unittest.TestCase):
    def setUp(self):
        self.mp3_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_MP3_AUDIO_FILE)
        self.flac_audio_file_name = get_absolute_path_for_project_file(__file__, TEST_FLAC_AUDIO_FILE)
        self.non_existing_file_path = "/tmp/non-existing-file-0"
        self.id3_audio_tag = Id3Tag(artist="Unknown Artist", title="Unknown Title", album="Unknown Album",
                                    date=2017, track=1, genre="Unknown Genre")

    def test_should_read_id3_tag_from_mp3(self):
        id3_tag_from_mp3 = read_audio_tag(self.mp3_audio_file_name)
        assert_that(id3_tag_from_mp3).is_equal_to(self.id3_audio_tag)

    def test_should_read_tag_from_flac(self):
        flac_audio_tag = read_audio_tag(self.flac_audio_file_name)
        assert_that(flac_audio_tag).is_equal_to(self.id3_audio_tag)

    def test_should_return_none_on_non_existing_file(self):
        id3_tag_from_wav = read_audio_tag(self.non_existing_file_path)
        assert_that(id3_tag_from_wav).is_none()

    def test_should_return_none_on_non_existing_tags(self):
        extracted_tags = read_audio_tag_using(self.non_existing_file_path, function_raising_error)
        assert_that(extracted_tags).is_none()
