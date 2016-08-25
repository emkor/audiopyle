import unittest

from assertpy import assert_that
from mock import Mock

from xtracter.model.audio_meta import AudioMeta
from xtracter.provider.audio_segment_provider import LocalAudioSegmentProvider
from xtracter.provider.plugin_provider import VampyPluginProvider
from xtracter.service.feature_extractor import FeatureExtractor
from xtracter.utils.xtracter_const import TEST_WAV_FILE_NAME, TEST_WAV_FILE_CHANNELS_COUNT, TEST_WAV_FILE_SAMPLE_RATE, \
    TEST_WAV_FILE_FRAME_COUNT, TEST_WAV_FILE_BIT_DEPTH
from xtracter.utils.xtracter_utils import XtracterUtils


class FeatureExtractorIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.mock_plugin_provider = Mock()
        test_segment_provider = LocalAudioSegmentProvider(XtracterUtils.get_test_resources_path())
        self.feature_extractor = FeatureExtractor(plugin_provider=self.mock_plugin_provider,
                                                  segment_provider=test_segment_provider)

    def test_should_analyze_with_first_plugin(self):
        test_file_audio_meta = AudioMeta(TEST_WAV_FILE_NAME,
                                         TEST_WAV_FILE_CHANNELS_COUNT,
                                         TEST_WAV_FILE_SAMPLE_RATE,
                                         TEST_WAV_FILE_FRAME_COUNT,
                                         TEST_WAV_FILE_BIT_DEPTH)
        self.mock_plugin_provider.get_all_plugins.return_value = [VampyPluginProvider().get_all_plugins()[0]]
        features = self.feature_extractor.extract(test_file_audio_meta)
        assert_that(features).is_not_empty()
