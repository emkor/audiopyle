import math
import unittest

from assertpy import assert_that

from commons.model.audio_meta import AudioMeta
from xtracter.provider.audio_segment_provider import LocalAudioSegmentProvider
from xtracter.service.audio_segment_reader import AudioSegmentReader
from xtracter.utils.xtracter_const import TEST_WAV_FILE_NAME, TEST_WAV_FILE_CHANNELS_COUNT, TEST_WAV_FILE_SAMPLE_RATE, \
    TEST_WAV_FILE_FRAME_COUNT, TEST_WAV_FILE_BIT_DEPTH, DEFAULT_BLOCK_SIZE
from xtracter.utils.xtracter_utils import XtracterUtils


class AudioSegmentReaderIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.segment_provider = LocalAudioSegmentProvider(XtracterUtils.get_test_resources_path())
        self.segment_reader = AudioSegmentReader(self.segment_provider)
        self.audio_meta = AudioMeta(TEST_WAV_FILE_NAME, TEST_WAV_FILE_CHANNELS_COUNT,
                                    TEST_WAV_FILE_SAMPLE_RATE, TEST_WAV_FILE_FRAME_COUNT,
                                    TEST_WAV_FILE_BIT_DEPTH)

    def test_should_read_test_wav_file_into_segments(self):
        segments = self.segment_reader.read_segments(self.audio_meta)
        assert_that(segments).is_not_none()
        assert_that(len(segments)).is_equal_to(
                math.ceil(TEST_WAV_FILE_FRAME_COUNT / float(DEFAULT_BLOCK_SIZE)))
        assert_that(segments[0].data).is_not_empty()

    def test_should_read_test_wav_file_into_equal_length_segments(self):
        segments = self.segment_reader.read_segments(self.audio_meta)
        lengths = set()
        for segment in segments:
            lengths.add(segment.length_frames())
        assert_that(lengths).is_not_empty().is_length(1)

    def test_should_read_test_wav_file_into_single_segment(self):
        segments = self.segment_reader.read_segments(self.audio_meta, block_size=None)
        assert_that(segments).is_not_none()
        assert_that(len(segments)).is_equal_to(1)
        assert_that(segments[0].data).is_not_empty()
