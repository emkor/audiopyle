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

    def to_dict(self):
        return self.__dict__


class AudioFeature(object):
    def __init__(self, audio_meta, segment_meta, plugin_key, plugin_output, raw_features):
        self.audio_meta = audio_meta
        self.segment_meta = segment_meta
        self.plugin_key = plugin_key
        self.plugin_output = plugin_output
        self.raw_features = raw_features

    def length_frames(self):
        return self.segment_meta.length

    def length_sec(self):
        return frames_to_sec(self.length_frames(), self.audio_meta.sample_rate)

    def next_offset(self):
        return self.segment_meta.offset + self.length_frames() + 1

    def to_dict(self):
        simple_dict = self.__dict__
        simple_dict.update({"audio_meta": self.audio_meta.to_dict()})
        simple_dict.update({"segment_meta": self.segment_meta.to_dict()})
        simple_dict.update({"raw_features": [feature.to_dict() for feature in self.raw_features]})
        return simple_dict

    def __str__(self):
        return "AudioFeature for {}:{} of an AudioFile: {} has {} raw features".format(self.plugin_key,
                                                                                       self.plugin_output,
                                                                                       self.audio_meta,
                                                                                       len(self.raw_features))

    def __repr__(self):
        return self.__str__()
