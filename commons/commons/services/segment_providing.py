from typing import Text

import numpy
from pydub import AudioSegment

from commons.utils.logger import get_logger

logger = get_logger()


def read_raw_audio_from_mp3(input_audio_file_path: Text) -> numpy.ndarray:
    int_samples = AudioSegment.from_file(input_audio_file_path, "mp3").set_channels(1).get_array_of_samples()
    return numpy.true_divide(int_samples, 32767.0)
