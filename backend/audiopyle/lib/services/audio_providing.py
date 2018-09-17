import numpy
from pydub import AudioSegment

from audiopyle.lib.utils.file_system import extract_extension
from audiopyle.lib.utils.logger import get_logger

logger = get_logger()


def read_raw_audio_from_file(input_audio_file_path: str) -> numpy.ndarray:
    mono_audio_segment = AudioSegment.from_file(input_audio_file_path,
                                                extract_extension(input_audio_file_path)).set_channels(1)
    normalized_mono_audio_segment = _normalize_to_maximum_dBFS(mono_audio_segment)
    return numpy.true_divide(normalized_mono_audio_segment.get_array_of_samples(), 32767.0)


def _match_target_loudness(sound: AudioSegment, target_dBFS: float) -> AudioSegment:
    # taken from https://github.com/jiaaro/pydub/issues/90
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def _normalize_to_maximum_dBFS(sound: AudioSegment) -> AudioSegment:
    # see https://github.com/jiaaro/pydub/blob/master/API.markdown#audiosegmentmax_dbfs
    return sound.apply_gain(-sound.max_dBFS)
