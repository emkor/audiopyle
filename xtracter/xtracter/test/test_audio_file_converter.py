import unittest

from assertpy import assert_that
from pydub import AudioSegment

from commons.service.file_accessor import FileAccessor
from xtracter.service.audio_file_converter import AudioFileConverter
from xtracter.utils.xtracter_utils import XtracterUtils
from xtracter.utils.xtracter_const import XtracterConst


class AudioFileConverterIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.converter = AudioFileConverter(
            XtracterUtils.get_test_resources_path(),
            XtracterUtils.get_test_resources_path())

    def test_should_convert_mp3_to_wav(self):
        self.converter.convert(XtracterConst.TEST_MP3_FILE_NAME)

        song = AudioSegment.from_wav(
            FileAccessor.join(
                XtracterUtils.get_test_resources_path(),
                XtracterConst.TEST_MP3_FILE_NAME + ".wav"))

        assert_that(
            FileAccessor.join(
                XtracterUtils.get_test_resources_path(),
                XtracterConst.TEST_MP3_FILE_NAME + ".wav")).exists()

        assert_that(song).is_instance_of(AudioSegment)
