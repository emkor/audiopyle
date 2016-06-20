# coding=utf-8
import logging

import vamp
from numpy import array
from xtracter.utils.xtracter_const import XtracterConst
from xtracter.model.feature import AudioFeature


class AudioSegmentAnalyzer(object):
    def __init__(self, vamp_lib=vamp):
        self.vamp_lib = vamp_lib

    def analyze_all(self, plugin_key, plugin_output, audio_segments):
        output = []
        for audio_segment in audio_segments:
            output.append(self.analyze(plugin_key, plugin_output, audio_segment))
        return output

    def analyze(self, plugin_key, plugin_output, audio_segment):
        try:
            return self.vamp_lib.collect(audio_segment.data, audio_segment.sample_rate, plugin_key, plugin_output)
        except Exception as e:
            logging.error(
                    "Error on analyzing segment with plugin key: {} output: {}. Details: {}".format(plugin_key,
                                                                                                    plugin_output,
                                                                                                    e))
            return None

    # deprecated
    def analyze_with_steps(self, audio_meta, audio_segments, plugin, plugin_output,
                           step_size=XtracterConst.DEFAULT_STEP_SIZE):
        output_features = []
        if plugin_output in plugin.outputs:
            vampy_input = self._cast_for_vampy(audio_segments)
            output_generator = self.vamp_lib.process_frames(vampy_input, audio_segments[0].sample_rate,
                                                            step_size, plugin.key, output=plugin_output)
            for i, raw_feature in enumerate(output_generator):
                raw_feature_value = raw_feature.get(XtracterConst.VAMPY_RAW_FEATURE_VALUES_KEY)
                raw_feature_label = raw_feature.get(XtracterConst.VAMPY_RAW_FEATURE_LABEL_KEY)
                audio_feature = AudioFeature(audio_meta, audio_segments[0].get_meta_of(),
                                             plugin, plugin_output, raw_feature_value, raw_feature_label)
                output_features.append(audio_feature)
            return output_features
        else:
            message = "Can not start analysis: no {} in output_features for plugin: {}"
            logging.error(message.format(plugin_output, plugin))
            return None

    # deprecated
    def _cast_for_vampy(self, audio_segments):
        # vampy expects to receive ndarray of blocks,
        # each block is ndarray of channels,
        # each channel is ndarray of float values
        # each value represents signal: [-1;1]
        vampy_casted_input = []
        for audio_segment in audio_segments:
            vampy_casted_input.append(array([audio_segment.data]))
        return array(vampy_casted_input)
