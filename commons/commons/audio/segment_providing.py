import struct
import wave
from typing import List

import numpy
from numpy import array

from commons.audio.file_meta import LocalAudioFileMeta
from commons.audio.segment import MonoAudioSegment
from commons.utils.logger import get_logger

logger = get_logger()


def read_segment(local_audio_file_meta: LocalAudioFileMeta) -> MonoAudioSegment:
    audio_frames = _read_raw_frames(local_audio_file_meta)
    if local_audio_file_meta.channels_count == 2:
        left, right = array(list(audio_frames[0::2])), array(list(audio_frames[1::2]))
        mono = [(l + r) / 2.0 for l, r in zip(left, right)]
    elif local_audio_file_meta.channels_count == 1:
        mono = audio_frames
    else:
        raise NotImplementedError("Can not read segment from such audio file: {}".format(local_audio_file_meta))
    return MonoAudioSegment(source_file_meta=local_audio_file_meta, frame_from=0,
                            frame_to=local_audio_file_meta.frames_count, data=numpy.asarray(mono))


def _read_raw_frames(local_audio_file_meta: LocalAudioFileMeta) -> List[float]:
    wav_file = wave.open(local_audio_file_meta.absolute_path, "r")
    binary_audio = wav_file.readframes(local_audio_file_meta.frames_count * local_audio_file_meta.channels_count)
    wav_file.close()
    audio_wave_as_int = list(
        struct.unpack_from("%dh" % local_audio_file_meta.frames_count * local_audio_file_meta.channels_count,
                           binary_audio))
    return [signal_value / 32767.0 for signal_value in audio_wave_as_int]
