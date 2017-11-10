import os
from commons.audio.file_meta import FileMeta
from commons.utils.conversion import utc_timestamp_to_datetime
import wave
from typing import Text, Optional

from commons.audio.file_meta import LocalAudioFileMeta
from commons.utils.conversion import B_to_b
from commons.utils.file_system import file_exists
from commons.utils.logger import get_logger


def get_file_meta(file_name: Text) -> FileMeta:
    file_stats = os.stat(file_name)
    last_access_utc = utc_timestamp_to_datetime(file_stats.st_atime)
    last_modification_utc = utc_timestamp_to_datetime(file_stats.st_mtime)
    created_on_utc = utc_timestamp_to_datetime(file_stats.st_ctime)
    return FileMeta(file_name=file_name, size=file_stats.st_size, last_access=last_access_utc,
                    last_modification=last_modification_utc, created_on=created_on_utc)


def read_audio_file_meta(absolute_path: Text) -> Optional[LocalAudioFileMeta]:
    if file_exists(absolute_path):
        audio_file = wave.open(f=absolute_path, mode="r")
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = audio_file.getparams()
        audio_file.close()
        return LocalAudioFileMeta(absolute_path=absolute_path, channels_count=nchannels, sample_rate=framerate,
                                  frames_count=nframes, bit_depth=B_to_b(sampwidth))
    return None
