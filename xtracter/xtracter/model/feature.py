from commons.utils.conversion import Converter


class AudioFeature(object):
    def __init__(self, audio_file_meta, audio_segment_meta, vampy_plugin, plugin_output, feature_value, label=''):
        self.audio_meta = audio_file_meta
        self.segment_meta = audio_segment_meta
        self.plugin = vampy_plugin
        self.plugin_output = plugin_output
        self.feature_value = feature_value
        self.label = label

    def length_frames(self):
        return self.segment_meta.length

    def length_sec(self):
        return Converter.frames_to_sec(self.length_frames(), self.audio_meta.sample_rate)

    def next_offset(self):
        return self.segment_meta.offset + self.length_frames() + 1
