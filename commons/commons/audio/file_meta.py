from typing import Text

from commons.abstractions.model import Model
from commons.utils.conversion import to_kilo, b_to_B, frames_to_sec, B_to_b


class AudioFileMeta(Model):
    def __init__(self, absolute_path: Text, channels_count: int, sample_rate: int, frames_count: int,
                 bit_depth: int) -> None:
        """Represents metadata of a raw audio file"""
        self.absolute_path = absolute_path
        self.channels_count = channels_count
        self.sample_rate = sample_rate
        self.frames_count = frames_count
        self.bit_depth = bit_depth

    def length_sec(self) -> float:
        return frames_to_sec(self.frames_count, self.sample_rate)

    def avg_kbps(self) -> float:
        return B_to_b(to_kilo(b_to_B(self.bit_depth) * self.channels_count * self.frames_count)) / self.length_sec()
