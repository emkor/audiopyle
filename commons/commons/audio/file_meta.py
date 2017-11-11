from typing import Text

from commons.abstractions.model import Model
from commons.utils.conversion import to_kilo, b_to_B, frames_to_sec, B_to_b


class AudioFileMeta(Model):
    def __init__(self, absolute_path: Text, file_size_bytes: int, channels_count: int, sample_rate: int) -> None:
        """Represents metadata of a raw audio file"""
        self.absolute_path = absolute_path
        self.channels_count = channels_count
        self.sample_rate = sample_rate
        self.file_size_bytes = file_size_bytes

    @property
    def length_sec(self) -> float:
        raise NotImplementedError()

    @property
    def bit_rate_kbps(self) -> float:
        raise NotImplementedError()


class WavAudioFileMeta(AudioFileMeta):
    def __init__(self, absolute_path: Text, file_size_bytes: int, channels_count: int, bit_depth: int,
                 sample_rate: int, frames_count: int) -> None:
        super().__init__(absolute_path, file_size_bytes, channels_count, sample_rate)
        self.frames_count = frames_count
        self.bit_depth = bit_depth

    @property
    def length_sec(self) -> float:
        return frames_to_sec(self.frames_count, self.sample_rate)

    @property
    def bit_rate_kbps(self) -> float:
        return B_to_b(to_kilo(b_to_B(self.bit_depth) * self.channels_count * self.frames_count)) / self.length_sec


class Mp3AudioFileMeta(AudioFileMeta):
    def __init__(self, absolute_path: Text, file_size_bytes: int, channels_count: int, sample_rate: int, length_sec: float,
                 bit_rate_kbps: float) -> None:
        super().__init__(absolute_path, file_size_bytes, channels_count, sample_rate)
        self.absolute_path = absolute_path
        self.channels_count = channels_count
        self.sample_rate = sample_rate
        self._length_sec = length_sec
        self._bit_rate_kbps = bit_rate_kbps

    @property
    def bit_rate_kbps(self) -> float:
        return self._bit_rate_kbps

    @property
    def length_sec(self) -> float:
        return self._length_sec

    def serialize(self):
        base_serialized = super().serialize()
        base_serialized.pop("_length_sec")
        base_serialized.pop("_bit_rate_kbps")
        base_serialized.update({"length_sec": self._length_sec,
                                "bit_rate_kbps": self._bit_rate_kbps})
        return base_serialized
