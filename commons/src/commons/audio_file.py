from common.abstraction import Model
from common.conversion import b_to_B, frames_to_sec, B_to_b
from common.conversion import to_kilo
from common.file_system import get_file_name


class AudioFileMeta(Model):
    def __init__(self, file_name, channels_count, sample_rate, frames_count, bit_depth):
        """
        Represents metadata of a raw audio file
        :type file_name: str
        :type channels_count: int
        :type sample_rate: int
        :type frames_count: int
        :type bit_depth: int
        """
        self.file_name = file_name
        self.channels_count = channels_count
        self.sample_rate = sample_rate
        self.frames_count = frames_count
        self.bit_depth = bit_depth

    def size_kB(self):
        """
        :rtype: float
        """
        return to_kilo(b_to_B(self.bit_depth) * self.channels_count * self.frames_count)

    def length_sec(self):
        """
        :rtype: float
        """
        return frames_to_sec(self.frames_count, self.sample_rate)

    def avg_kbps(self):
        """
        :rtype: float
        """
        return B_to_b(self.size_kB()) / self.length_sec()


class LocalAudioFileMeta(AudioFileMeta):
    def __init__(self, absolute_path, channels_count, sample_rate, frames_count, bit_depth):
        """
        Represents metadata of a raw audio file
        :type absolute_path: str
        :type channels_count: int
        :type sample_rate: int
        :type frames_count: int
        :type bit_depth: int
        """
        super(LocalAudioFileMeta, self).__init__(get_file_name(absolute_path), channels_count, sample_rate,
                                                 frames_count, bit_depth)
        self.absolute_path = absolute_path
