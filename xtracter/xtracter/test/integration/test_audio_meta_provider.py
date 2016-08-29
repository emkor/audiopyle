import unittest
from assertpy import assert_that
from xtracter.provider.audio_meta_provider import LocalAudioMetaProvider
from xtracter.utils.xtracter_const import TEST_WAV_FILE_NAME, TEST_WAV_FILE_CHANNELS_COUNT, \
    TEST_WAV_FILE_BIT_DEPTH, TEST_WAV_FILE_SAMPLE_RATE, TEST_WAV_FILE_FRAME_COUNT
from xtracter.utils.xtracter_utils import XtracterUtils


class LocalAudioMetaProviderIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.test_file_path = XtracterUtils.get_test_wav_file_path()
        self.meta_provider = LocalAudioMetaProvider()

    def test_reading_audio_meta(self):
        audio_meta = self.meta_provider.read_meta_from(self.test_file_path)
        assert_that(audio_meta).is_not_none()
        assert_that(audio_meta.filename).is_equal_to(TEST_WAV_FILE_NAME)
        assert_that(audio_meta.channels_count).is_equal_to(TEST_WAV_FILE_CHANNELS_COUNT)
        assert_that(audio_meta.bit_depth).is_equal_to(TEST_WAV_FILE_BIT_DEPTH)
        assert_that(audio_meta.sample_rate).is_equal_to(TEST_WAV_FILE_SAMPLE_RATE)
        assert_that(audio_meta.frames_count).is_equal_to(TEST_WAV_FILE_FRAME_COUNT)
