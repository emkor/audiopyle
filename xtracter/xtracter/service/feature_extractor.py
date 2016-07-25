from xtracter.model.feature import AudioFeature, RawFeature
from xtracter.provider.audio_segment_provider import LocalAudioSegmentProvider
from xtracter.provider.plugin_provider import VampyPluginProvider
from xtracter.service.segment_analyzer import AudioSegmentAnalyzer
from xtracter.utils.xtracter_const import XtracterConst


class FeatureExtractor(object):
    def __init__(self, segment_provider=None, plugin_provider=None, segment_analyzer=None):
        """
        Service for actual feature extraction
        :type segment_provider: xtracter.provider.audio_segment_provider.LocalAudioSegmentProvider
        :type plugin_provider: xtracter.provider.plugin_provider.VampyPluginProvider
        :type segment_analyzer: xtracter.service.segment_analyzer.AudioSegmentAnalyzer
        :rtype: xtracter.service.feature_extractor.FeatureExtractor
        """
        self.segment_provider = segment_provider or LocalAudioSegmentProvider(XtracterConst.AUDIO_FILES_CACHE_PATH)
        self.plugin_provider = plugin_provider or VampyPluginProvider()
        self.segment_analyzer = segment_analyzer or AudioSegmentAnalyzer()

    def extract(self, audio_file_meta):
        """
        Extracts list of features from given file meta
        :type audio_file_meta: xtracter.model.audio_meta.AudioMeta
        :rtype: list[xtracter.model.feature.AudioFeature]
        """
        plugins = self.plugin_provider.get_all_plugins()
        audio_features = []
        segment = self.segment_provider.read_segment(audio_file_meta)
        for plugin in plugins:
            for plugin_output in plugin.outputs:
                plugin_feature = self._extract_feature(audio_file_meta, plugin, plugin_output, segment)
                audio_features.append(plugin_feature)
        return audio_features

    def _extract_feature(self, audio_file_meta, plugin, plugin_output, segment):
        raw_features_dicts = self.segment_analyzer.analyze(plugin.key, plugin_output, segment)
        raw_features = RawFeature.from_dict_list(raw_features_dicts)
        return AudioFeature(audio_file_meta, segment.get_meta_of(), plugin, plugin_output, raw_features)
