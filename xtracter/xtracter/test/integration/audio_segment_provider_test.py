import unittest
from numpy.testing import assert_array_almost_equal
from assertpy import assert_that
from xtracter.model.audio_meta import AudioMeta
from xtracter.provider.audio_segment_provider import LocalAudioSegmentProvider
from xtracter.utils.xtracter_const import XtracterConst
from xtracter.utils.xtracter_utils import XtracterUtils


class LocalAudioSegmentProviderIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.segment_provider = LocalAudioSegmentProvider(XtracterUtils.get_test_resources_path())
        self.test_file_audio_meta = AudioMeta(XtracterConst.TEST_WAV_FILE_NAME,
                                              XtracterConst.TEST_WAV_FILE_CHANNELS_COUNT,
                                              XtracterConst.TEST_WAV_FILE_SAMPLE_RATE,
                                              XtracterConst.TEST_WAV_FILE_FRAME_COUNT,
                                              XtracterConst.TEST_WAV_FILE_BIT_DEPTH)

    def test_read_file(self):
        audio_segment = self.segment_provider.read_segment(self.test_file_audio_meta)
        assert_that(audio_segment).is_not_none()
        assert_that(audio_segment.offset).is_equal_to(0)
        assert_that(audio_segment.next_offset()).is_equal_to(self.test_file_audio_meta.frames_count + 1)
        assert_that(audio_segment.length_frames()).is_equal_to(self.test_file_audio_meta.frames_count)
        assert_that(audio_segment.sample_rate).is_equal_to(self.test_file_audio_meta.sample_rate)

    def test_audio_signal_min_max_value(self):
        audio_segment = self.segment_provider.read_segment(self.test_file_audio_meta)
        min_value = min(audio_segment.data)
        max_value = max(audio_segment.data)
        assert_that(min_value >= -1.0).is_true()
        assert_that(max_value <= 1.0).is_true()

    def test_read_file_precision(self):
        audio_segment = self.segment_provider.read_segment(self.test_file_audio_meta)
        expected_audio_data = XtracterUtils.import_test_file_csv_data()
        assert_that(len(audio_segment.data)).is_equal_to(len(expected_audio_data))
        assert_array_almost_equal(audio_segment.data, expected_audio_data, decimal=4)
