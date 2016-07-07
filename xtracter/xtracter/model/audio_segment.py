from commons.utils.conversion import Converter


class AudioSegmentMeta(object):
    def __init__(self, sample_rate, length, offset=0):
        self.sample_rate = sample_rate
        self.length = length
        self.offset = offset

    def length_frames(self):
        return self.length

    def length_sec(self):
        return Converter.frames_to_sec(self.length_frames(), self.sample_rate)

    def next_offset(self):
        return self.offset + self.length_frames() + 1


class AudioSegment(AudioSegmentMeta):
    def __init__(self, data, sample_rate, offset=0):
        super(AudioSegment, self).__init__(sample_rate, len(data), offset)
        self.data = data

    def get_meta_of(self):
        return AudioSegmentMeta(self.sample_rate, self.length, self.offset)
