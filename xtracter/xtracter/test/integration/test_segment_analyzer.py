import unittest
from assertpy import assert_that

from xtracter.model.audio_meta import AudioMeta
from xtracter.provider.audio_segment_provider import LocalAudioSegmentProvider
from xtracter.provider.plugin_provider import VampyPluginProvider
from xtracter.service.audio_segment_reader import AudioSegmentReader
from xtracter.service.segment_analyzer import AudioSegmentAnalyzer
from xtracter.utils.xtracter_const import XtracterConst
from xtracter.utils.xtracter_utils import XtracterUtils


class AudioSegmentAnalyzerIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.audio_segments = self._init_test()
        self.analyzer = AudioSegmentAnalyzer()
        self.plugins = VampyPluginProvider().get_all_plugins()

    def test_analysis_on_single_segment_with_first_plugin(self):
        segment = self.audio_segments[0]
        plugin = self.plugins[0]
        plugin_output = plugin.outputs[0]
        feature = self.analyzer.analyze(plugin.key, plugin_output, segment)
        assert_that(feature).is_not_none()

    def test_analysis_on_multiple_semgents_with_first_plugin(self):
        plugin = self.plugins[0]
        plugin_output = plugin.outputs[0]
        features = [self.analyzer.analyze(plugin.key, plugin_output, segment) for segment in self.audio_segments]
        assert_that(features).is_not_none().is_not_empty().is_length(len(self.audio_segments))

    def test_analysis_on_single_semgent_with_multiple_plugins(self):
        segment = self.audio_segments[0]
        result_dict = {}
        for plugin in self.plugins[0:15]:
            result_dict.update({plugin.key: {}})
            for output in plugin.outputs:
                result_dict.get(plugin.key).update({output: self.analyzer.analyze(plugin.key, output, segment)})
        assert_that(result_dict).is_not_none().is_not_empty()

    def _init_test(self):
        audio_segment_reader = AudioSegmentReader(
            LocalAudioSegmentProvider(XtracterUtils.get_test_resources_path()))
        test_file_meta = AudioMeta(XtracterConst.TEST_WAV_FILE_NAME, XtracterConst.TEST_WAV_FILE_CHANNELS_COUNT,
                                   XtracterConst.TEST_WAV_FILE_SAMPLE_RATE, XtracterConst.TEST_WAV_FILE_FRAME_COUNT,
                                   XtracterConst.TEST_WAV_FILE_BIT_DEPTH)
        return audio_segment_reader.read_segments(test_file_meta)
