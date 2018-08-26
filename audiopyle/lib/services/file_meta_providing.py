from typing import Optional

import os
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

from audiopyle.lib.models.file_meta import CompressedAudioFileMeta, FileMeta
from audiopyle.lib.services.audio_tag_providing import Extension
from audiopyle.lib.utils.conversion import to_kilo, utc_timestamp_to_datetime
from audiopyle.lib.utils.file_system import file_exists, file_size_bytes, get_file_name, extract_extension
from audiopyle.lib.utils.logger import get_logger

logger = get_logger()


def read_file_meta(file_name: str) -> Optional[FileMeta]:
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


def read_audio_file_meta(absolute_path: str) -> Optional[CompressedAudioFileMeta]:
    if file_exists(absolute_path):
        audio_file = None
        audio_file_size = file_size_bytes(absolute_path)
        try:
            if extract_extension(absolute_path) == Extension.MP3.value:
                return _read_mp3_file_meta(absolute_path, audio_file_size)
            elif extract_extension(absolute_path) == Extension.FLAC.value:
                return _read_flac_file_meta(absolute_path, audio_file_size)
        except Exception as e:
            logger.exception("Could not read audio file meta from {}. Details: {}".format(absolute_path, e))
            if audio_file:
                audio_file.close()
    return None


def _read_mp3_file_meta(absolute_path: str, audio_file_size: int) -> CompressedAudioFileMeta:
    mp3 = MP3(filename=absolute_path)
    return CompressedAudioFileMeta(file_name=get_file_name(absolute_path), file_size_bytes=audio_file_size,
                                   channels_count=mp3.info.channels, sample_rate=mp3.info.sample_rate,
                                   bit_rate_kbps=to_kilo(mp3.info.bitrate), length_sec=mp3.info.length)


def _read_flac_file_meta(absolute_path, audio_file_size) -> CompressedAudioFileMeta:
    flac = FLAC(filename=absolute_path)
    return CompressedAudioFileMeta(file_name=get_file_name(absolute_path), file_size_bytes=audio_file_size,
                                   channels_count=flac.info.channels, sample_rate=flac.info.sample_rate,
                                   bit_rate_kbps=to_kilo(flac.info.bitrate), length_sec=flac.info.length)
