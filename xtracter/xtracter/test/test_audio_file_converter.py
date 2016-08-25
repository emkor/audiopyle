import logging
import unittest

from assertpy import assert_that
from pydub import AudioSegment

from commons.service.file_accessor import FileAccessor
from xtracter.service.audio_file_converter import AudioFileConverter
from xtracter.utils.xtracter_utils import XtracterUtils
from xtracter.utils.xtracter_const import XtracterConst

LOGGER_NAME = "xtracter"


class AudioFileConverterIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger = logging.getLogger(LOGGER_NAME)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)s | %(asctime)s | %(levelname)s | %(funcName)s | %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def setUp(self):
        self.converter = AudioFileConverter(
            XtracterUtils.get_test_resources_path(),
            XtracterUtils.get_test_resources_path())

    def test_should_convert_mp3_to_wav(self):
        self.converter.convert(XtracterConst.TEST_MP3_FILE_NAME)

        output_file_path = FileAccessor.join(
            XtracterUtils.get_test_resources_path(),
            XtracterConst.TEST_MP3_FILE_NAME + ".wav")

        song = AudioSegment.from_wav(output_file_path)

        assert_that(output_file_path).exists()
        assert_that(song).is_instance_of(AudioSegment)
