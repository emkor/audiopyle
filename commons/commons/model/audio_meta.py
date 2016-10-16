from copy import deepcopy

from commons.utils.conversion import b_to_B, B_to_b, to_kilo, frames_to_sec


class AudioMeta(object):
    @staticmethod
    def from_dict(audio_meta_dict):
        """
        :type audio_meta_dict: dict
        :rtype: commons.model.audio_meta.AudioMeta
        """
        return AudioMeta(**audio_meta_dict)

    def __init__(self, filename, channels_count, sample_rate, frames_count, bit_depth):
        self.filename = filename
        self.channels_count = channels_count
        self.sample_rate = sample_rate
        self.frames_count = frames_count
        self.bit_depth = bit_depth

    def size_kB(self):
        return to_kilo(b_to_B(self.bit_depth) * self.channels_count * self.frames_count)

    def length_sec(self):
        return frames_to_sec(self.frames_count, self.sample_rate)

    def avg_kbps(self):
        return B_to_b(self.size_kB()) / self.length_sec()

    def to_dict(self):
        return deepcopy(self.__dict__)

    def __str__(self):
        return "AudioMeta: {}".format(self.__dict__)

    def __repr__(self):
        return self.__str__()
