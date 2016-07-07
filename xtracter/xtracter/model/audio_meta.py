from commons.utils.conversion import Converter


class AudioMeta(object):
    def __init__(self, filename, channels_count, sample_rate, frames_count, bit_depth):
        self.filename = filename
        self.channels_count = channels_count
        self.sample_rate = sample_rate
        self.frames_count = frames_count
        self.bit_depth = bit_depth

    def size_kB(self):
        return Converter.to_kilo(Converter.b_to_B(self.bit_depth) * self.channels_count * self.frames_count)

    def length_sec(self):
        return Converter.frames_to_sec(self.frames_count, self.sample_rate)

    def avg_kbps(self):
        return Converter.B_to_b(self.size_kB()) / self.length_sec()
