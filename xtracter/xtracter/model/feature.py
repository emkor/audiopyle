from commons.utils.conversion import frames_to_sec


class RawFeature(object):
    def __init__(self, timestamp, value, label=''):
        self.timestamp = timestamp
        self.value = value
        self.label = label

    def __str__(self):
        return "RawFeature for {}s labeled as {} has values: {}".format(self.timestamp, self.label, self.value)

    def __repr__(self):
        return self.__str__()


class AudioFeature(object):
    def __init__(self, audio_file_meta, audio_segment_meta, vamp_plugin, plugin_output, raw_features):
        self.audio_meta = audio_file_meta
        self.segment_meta = audio_segment_meta
        self.plugin = vamp_plugin
        self.plugin_output = plugin_output
        self.raw_features = raw_features

    def length_frames(self):
        return self.segment_meta.length

    def length_sec(self):
        return frames_to_sec(self.length_frames(), self.audio_meta.sample_rate)

    def next_offset(self):
        return self.segment_meta.offset + self.length_frames() + 1

    def __str__(self):
        return "AudioFeature for {} [{} output] of an AudioFile: {} has {} of raws".format(self.plugin,
                                                                                           self.plugin_output,
                                                                                           self.audio_meta,
                                                                                           len(self.raw_features))

    def __repr__(self):
        return self.__str__()
