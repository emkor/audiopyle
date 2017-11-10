import os
from datetime import datetime
from typing import Text

from commons.abstractions.model import Model
from commons.utils.conversion import utc_timestamp_to_datetime, to_kilo, to_mega, b_to_B, frames_to_sec, B_to_b
from commons.utils.file_system import extract_extension, get_file_name


class FileMeta(Model):
    def __init__(self, file_name: Text, size: int, last_access: datetime, last_modification: datetime,
                 created_on: datetime) -> None:
        self.created_on = created_on
        self.last_modification = last_modification
        self.last_access = last_access
        self.size = size
        self.file_name = file_name

    @property
    def size_kB(self) -> float:
        return to_kilo(self.size)

    @property
    def size_mB(self) -> float:
        return to_mega(self.size)

    @property
    def file_base_name(self) -> Text:
        return get_file_name(self.file_name)

    @property
    def extension(self) -> Text:
        return extract_extension(self.file_name)





class LocalAudioFileMeta(Model):
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
