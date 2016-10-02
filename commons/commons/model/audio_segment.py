from commons.utils.conversion import frames_to_sec


class AudioSegmentMeta(object):
    @staticmethod
    def from_dict(audio_segment_meta_dict):
        """
        :type audio_segment_meta_dict: dict
        :rtype: commons.model.audio_segment.AudioSegmentMeta
        """
        return AudioSegmentMeta(**audio_segment_meta_dict)

    def __init__(self, sample_rate, length, offset=0):
        self.sample_rate = sample_rate
        self.length = length
        self.offset = offset

    def length_frames(self):
        return self.length

    @property
    def length_sec(self):
        return frames_to_sec(self.length_frames(), self.sample_rate)

    def next_offset(self):
        return self.offset + self.length_frames() + 1

    def to_dict(self):
        return self.__dict__

    def __str__(self):
        return "AudioSegmentMeta: {}".format(self.__dict__)

    def __repr__(self):
        self.__str__()


class AudioSegment(AudioSegmentMeta):
    @staticmethod
    def from_dict(audio_segment_dict):
        """
        :type audio_segment_dict: dict
        :rtype: commons.model.audio_segment.AudioSegment
        """
        return AudioSegment(**audio_segment_dict)

    def __init__(self, data, sample_rate, offset=0):
        super(AudioSegment, self).__init__(sample_rate, len(data), offset)
        self.data = data

    def get_meta_of(self):
        return AudioSegmentMeta(self.sample_rate, self.length, self.offset)

    def to_dict(self):
        return self.__dict__
