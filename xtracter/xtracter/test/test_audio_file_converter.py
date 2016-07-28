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
            XtracterUtils.get_test_resources_path())

    def test_should_be_equal(self):
        self.converter.convert(XtracterUtils.get_test_mp3_file_name())

        song = AudioSegment.from_wav(
            FileAccessor.join(
                XtracterUtils.get_test_resources_path(),
                XtracterUtils.get_test_mp3_file_name() + ".wav"))

        assert_that(song).is_instance_of(AudioSegment)
