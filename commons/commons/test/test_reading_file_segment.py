import unittest

from assertpy import assert_that

from commons.services.file_meta_providing import read_wav_file_meta
from commons.services.segment_providing import read_wav_segment
from commons.test.utils import get_absolute_path_for_project_file, TEST_WAV_AUDIO_FILE


class TestReadingFileSegments(unittest.TestCase):
    def setUp(self):
        self.file_meta = read_wav_file_meta(get_absolute_path_for_project_file(__file__, TEST_WAV_AUDIO_FILE))

    def test_should_read_segment(self):
        audio_segment = read_wav_segment(self.file_meta)
        assert_that(audio_segment).is_not_none()
