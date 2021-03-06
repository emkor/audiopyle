from datetime import datetime
from typing import Dict, Any

from audiopyle.lib.abstractions.model import Model
from audiopyle.lib.utils.conversion import to_kilo, to_mega, utc_datetime_to_iso_format, utc_iso_format_to_datetime
from audiopyle.lib.utils.file_system import extract_extension


class FileMeta(Model):
    def __init__(self, file_name: str, size: int, last_access: datetime, last_modification: datetime,
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
    def extension(self) -> str:
        return extract_extension(self.file_name)

    def to_serializable(self):
        base_serialized = super().to_serializable()
        base_serialized.update({"created_on": utc_datetime_to_iso_format(self.created_on),
                                "last_modification": utc_datetime_to_iso_format(self.last_modification),
                                "last_access": utc_datetime_to_iso_format(self.last_access)})
        return base_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[str, Any]):
        serialized.update({
            "created_on": utc_iso_format_to_datetime(serialized["created_on"]),
            "last_modification": utc_iso_format_to_datetime(serialized["last_modification"]),
            "last_access": utc_iso_format_to_datetime(serialized["last_access"])
        })
        return FileMeta(**serialized)


class AudioFileMeta(Model):
    def __init__(self, file_name: str, file_size_bytes: int, channels_count: int, sample_rate: int) -> None:
        """Represents metadata of a raw audio file"""
        self.file_name = file_name
        self.channels_count = channels_count
        self.sample_rate = sample_rate
        self.file_size_bytes = file_size_bytes

    @property
    def length_sec(self) -> float:
        raise NotImplementedError()

    @property
    def bit_rate_kbps(self) -> float:
        raise NotImplementedError()


class CompressedAudioFileMeta(AudioFileMeta):
    def __init__(self, file_name: str, file_size_bytes: int, channels_count: int, sample_rate: int,
                 length_sec: float, bit_rate_kbps: float) -> None:
        super().__init__(file_name, file_size_bytes, channels_count, sample_rate)
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
