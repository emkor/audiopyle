import wave
from typing import Text, Optional

import os
from mutagen.mp3 import MP3

from commons.audio.file_meta import WavAudioFileMeta, Mp3AudioFileMeta, FileMeta
from commons.utils.conversion import B_to_b, to_kilo, utc_timestamp_to_datetime
from commons.utils.file_system import file_exists, file_size_bytes, get_file_name
from commons.utils.logger import get_logger

logger = get_logger()


def read_file_meta(file_name: Text) -> Optional[FileMeta]:
    if file_exists(file_name):
        file_stats = os.stat(file_name)
        last_access_utc = utc_timestamp_to_datetime(file_stats.st_atime)
        last_modification_utc = utc_timestamp_to_datetime(file_stats.st_mtime)
        created_on_utc = utc_timestamp_to_datetime(file_stats.st_ctime)
        return FileMeta(file_name=get_file_name(file_name), size=file_stats.st_size, last_access=last_access_utc,
                        last_modification=last_modification_utc, created_on=created_on_utc)
    else:
        logger.warning("Requested file {} does not exist".format(file_name))
        return None


def read_wav_file_meta(absolute_path: Text) -> Optional[WavAudioFileMeta]:
    if file_exists(absolute_path):
        audio_file = None
        audio_file_size = file_size_bytes(absolute_path)
        try:
            audio_file = wave.open(f=absolute_path, mode="r")
            (nchannels, sampwidth, framerate, nframes, comptype, compname) = audio_file.getparams()
            audio_file.close()
            return WavAudioFileMeta(absolute_path=absolute_path, file_size_bytes=audio_file_size,
                                    channels_count=nchannels,
                                    bit_depth=B_to_b(sampwidth), sample_rate=framerate, frames_count=nframes)
        except Exception as e:
            logger.exception("Could not read audio file meta from {}. Details: {}".format(absolute_path, e))
            if audio_file:
                audio_file.close()
    return None


def read_mp3_file_meta(absolute_path: Text) -> Optional[Mp3AudioFileMeta]:
    if file_exists(absolute_path):
        audio_file = None
        audio_file_size = file_size_bytes(absolute_path)
        try:
            mp3 = MP3(filename=absolute_path)
            return Mp3AudioFileMeta(absolute_path=absolute_path, file_size_bytes=audio_file_size,
                                    channels_count=mp3.info.channels, sample_rate=mp3.info.sample_rate,
                                    bit_rate_kbps=to_kilo(mp3.info.bitrate), length_sec=mp3.info.length)
        except Exception as e:
            logger.exception("Could not read audio file meta from {}. Details: {}".format(absolute_path, e))
            if audio_file:
                audio_file.close()
    return None
