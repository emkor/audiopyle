import unittest

from assertpy import assert_that
from numpy.core.multiarray import ndarray

from commons.services.file_meta_providing import read_wav_file_meta
from commons.services.segment_providing import read_wav_segment
from commons.test.utils import get_absolute_path_for_project_file, TEST_WAV_AUDIO_FILE


class TestReadingFileSegments(unittest.TestCase):
    def setUp(self):
        self.file_meta = read_wav_file_meta(get_absolute_path_for_project_file(__file__, TEST_WAV_AUDIO_FILE))

    def test_should_read_segment(self):
        audio_segment = read_wav_segment(self.file_meta)
        assert_that(audio_segment).is_not_none()
        assert_that(audio_segment.data.size).is_equal_to(103936)
        assert_that(audio_segment.data).is_instance_of(ndarray)
        assert_that(audio_segment.frame_from).is_equal_to(0)
        assert_that(audio_segment.frame_to).is_equal_to(103936)
        assert_that(audio_segment.source_file_meta).is_equal_to(self.file_meta)
