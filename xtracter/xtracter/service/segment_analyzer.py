# coding=utf-8
import logging
import vamp


class AudioSegmentAnalyzer(object):
    def __init__(self, vamp_lib=vamp):
        self.vamp_lib = vamp_lib
        self.logger = logging.getLogger(__name__)

    def analyze_all(self, plugin_key, plugin_output, audio_segments):
        output = []
        for audio_segment in audio_segments:
            output.append(self.analyze(plugin_key, plugin_output, audio_segment))
        return output

    def analyze(self, plugin_key, plugin_output, audio_segment):
        try:
            return self.vamp_lib.collect(audio_segment.data, audio_segment.sample_rate, plugin_key, plugin_output)
        except Exception as e:
            self.logger.exception(
                "Error on analyzing segment with plugin key: {} output: {}. Details: {}"
                .format(plugin_key, plugin_output, e))
            return None
