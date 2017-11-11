import wave
from typing import Text, Optional

from commons.audio.file_meta import AudioFileMeta
from commons.utils.conversion import B_to_b
from commons.utils.file_system import file_exists
from commons.utils.logger import get_logger

logger = get_logger()


def read_audio_file_meta(absolute_path: Text) -> Optional[AudioFileMeta]:
    if file_exists(absolute_path):
        audio_file = None
        try:
            audio_file = wave.open(f=absolute_path, mode="r")
            (nchannels, sampwidth, framerate, nframes, comptype, compname) = audio_file.getparams()
            audio_file.close()
            return AudioFileMeta(absolute_path=absolute_path, channels_count=nchannels, sample_rate=framerate,
                                 frames_count=nframes, bit_depth=B_to_b(sampwidth))
        except Exception as e:
            logger.exception("Could not read audio file meta from {}. Details: {}".format(absolute_path, e))
            if audio_file:
                audio_file.close()
    return None


def read_mp3_meta(absolute_path: Text) -> Optional[AudioFileMeta]:
    if file_exists(absolute_path):
        audio_file = None
        try:
            audio_file = wave.open(f=absolute_path, mode="r")
            (nchannels, sampwidth, framerate, nframes, comptype, compname) = audio_file.getparams()
            audio_file.close()
            return AudioFileMeta(absolute_path=absolute_path, channels_count=nchannels, sample_rate=framerate,
                                 frames_count=nframes, bit_depth=B_to_b(sampwidth))
        except Exception as e:
            logger.exception("Could not read audio file meta from {}. Details: {}".format(absolute_path, e))
            if audio_file:
                audio_file.close()
    return None