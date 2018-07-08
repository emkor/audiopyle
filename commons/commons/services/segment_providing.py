import numpy
from pydub import AudioSegment

from commons.utils.file_system import extract_extension
from commons.utils.logger import get_logger

logger = get_logger()


def read_raw_audio_from_file(input_audio_file_path: str) -> numpy.ndarray:
    int_samples = AudioSegment.from_file(input_audio_file_path, extract_extension(input_audio_file_path))\
        .set_channels(1)\
        .get_array_of_samples()
    return numpy.true_divide(int_samples, 32767.0)
