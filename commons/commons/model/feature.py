from commons.model.audio_meta import AudioMeta
from commons.model.audio_segment import AudioSegmentMeta
from commons.utils.conversion import frames_to_sec


class RawFeature(object):
    @staticmethod
    def from_dict(raw_feature_dict):
        """
        :type raw_feature_dict: dict
        :rtype: commons.model.feature.RawFeature
        """
        return RawFeature(**raw_feature_dict)

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
    @staticmethod
    def from_dict(audio_feature_dict):
        """
        :type audio_feature_dict: dict
        :rtype: commons.model.feature.AudioFeature
        """
        raw_features = [RawFeature.from_dict(raw_feature) for raw_feature in audio_feature_dict.get("raw_features")]
        segment_meta = AudioSegmentMeta.from_dict(audio_feature_dict.get("segment_meta"))
        audio_meta = AudioMeta.from_dict(audio_feature_dict.get("audio_meta"))
        return AudioFeature(audio_meta=audio_meta, segment_meta=segment_meta,
                            plugin_key=audio_feature_dict.get("plugin_key"),
                            plugin_output=audio_feature_dict.get("plugin_output"), raw_features=raw_features)

    def __init__(self, audio_meta, segment_meta, plugin_key, plugin_output, raw_features):
        """
        :type audio_meta: commons.model.audio_meta.AudioMeta
        :type segment_meta: commons.model.audio_segment.AudioSegmentMeta
        :type plugin_key: str
        :type plugin_output: str
        :type raw_features: list[commons.model.feature.RawFeature]
        """
        self.audio_meta = audio_meta
        self.segment_meta = segment_meta
        self.plugin_key = plugin_key
        self.plugin_output = plugin_output
        self.raw_features = raw_features

    def length_frames(self):
        """
        :rtype: int
        """
        return self.segment_meta.length

    def length_sec(self):
        """
        :rtype: float
        """
        return frames_to_sec(self.length_frames(), self.audio_meta.sample_rate)

    def next_offset(self):
        """
        :rtype: int
        """
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
