import unittest

from assertpy import assert_that
from pydub import AudioSegment

from commons.service.file_accessor import FileAccessor
from xtracter.service.audio_file_converter import AudioFileConverter
from xtracter.utils.xtracter_utils import XtracterUtils


class AudioFileConverterIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.converter = AudioFileConverter(
            XtracterUtils.get_test_resources_path(),
            XtracterUtils.get_wav_file_path())

    def test_should_be_equal(self):
        song_a = AudioSegment.from_file(
            XtracterUtils.get_test_converted_wav_file_path(),
            format="wav")

        self.converter.convert(XtracterUtils.get_test_mp3_file_name())

        song_b = AudioSegment.from_file(
            FileAccessor.join(
                XtracterUtils.get_wav_file_path(),
                XtracterUtils.get_test_mp3_file_name() + ".wav"),
            format="wav")

        assert_that(song_a).is_equal_to(song_b)
