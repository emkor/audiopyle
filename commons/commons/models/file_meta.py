from datetime import datetime
from typing import Text, Dict, Any

from commons.abstractions.model import Model
from commons.utils.conversion import to_kilo, b_to_B, frames_to_sec, B_to_b, to_mega, utc_datetime_to_timestamp, \
    utc_timestamp_to_datetime
from commons.utils.file_system import extract_extension


class FileMeta(Model):
    def __init__(self, file_name: Text, size: int, last_access: datetime, last_modification: datetime,
                 created_on: datetime) -> None:
        self.file_name = file_name
        self.created_on = created_on
        self.last_modification = last_modification
        self.last_access = last_access
        self.size = size

    @property
    def size_kB(self) -> float:
        return to_kilo(self.size)

    @property
    def size_mB(self) -> float:
        return to_mega(self.size)

    @property
    def extension(self) -> Text:
        return extract_extension(self.file_name)

    def to_serializable(self):
        base_serialized = super().to_serializable()
        base_serialized.update({"created_on": utc_datetime_to_timestamp(self.created_on),
                                "last_modification": utc_datetime_to_timestamp(self.last_modification),
                                "last_access": utc_datetime_to_timestamp(self.last_access)})
        return base_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[Text, Any]):
        serialized.update({
            "created_on": utc_timestamp_to_datetime(serialized["created_on"]),
            "last_modification": utc_timestamp_to_datetime(serialized["last_modification"]),
            "last_access": utc_timestamp_to_datetime(serialized["last_access"])
        })
        return FileMeta(**serialized)


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
        return round(frames_to_sec(self.frames_count, self.sample_rate), 3)

    @property
    def bit_rate_kbps(self) -> float:
        return round(
            B_to_b(to_kilo(b_to_B(self.bit_depth) * self.channels_count * self.frames_count)) / self.length_sec,
            ndigits=1)


class Mp3AudioFileMeta(AudioFileMeta):
    def __init__(self, absolute_path: Text, file_size_bytes: int, channels_count: int, sample_rate: int,
                 length_sec: float, bit_rate_kbps: float) -> None:
        super().__init__(absolute_path, file_size_bytes, channels_count, sample_rate)
        self._length_sec = length_sec
        self._bit_rate_kbps = bit_rate_kbps

    @property
    def bit_rate_kbps(self) -> float:
        return round(self._bit_rate_kbps, ndigits=1)

    @property
    def length_sec(self) -> float:
        return round(self._length_sec, ndigits=3)

    def to_serializable(self):
        base_serialized = super().to_serializable()
        base_serialized.pop("_length_sec")
        base_serialized.pop("_bit_rate_kbps")
        base_serialized.update({"length_sec": self._length_sec,
                                "bit_rate_kbps": self._bit_rate_kbps})
        return base_serialized
