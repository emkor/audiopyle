import wave
from typing import Text, Optional

from commons.audio.file_meta import LocalAudioFileMeta
from commons.utils.conversion import B_to_b
from commons.utils.file_system import file_exists


def read_audio_file_meta(absolute_path: Text) -> Optional[LocalAudioFileMeta]:
    if file_exists(absolute_path):
        audio_file = wave.open(f=absolute_path, mode="r")
        (nchannels, sampwidth, framerate, nframes, comptype, compname) = audio_file.getparams()
        audio_file.close()
        return LocalAudioFileMeta(absolute_path=absolute_path, channels_count=nchannels, sample_rate=framerate,
                                  frames_count=nframes, bit_depth=B_to_b(sampwidth))
    return None
