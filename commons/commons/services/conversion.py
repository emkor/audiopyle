from typing import Text

import os
from pydub import AudioSegment

from commons.utils.file_system import TMP_DIR
from commons.utils.logger import get_logger

logger = get_logger()


def generate_output_wav_file_path(task_id: Text) -> Text:
    return "{}.wav".format(os.path.join(TMP_DIR, task_id))


def convert_to_wav(compressed_audio_file_absolute_path: Text, output_file_path: Text) -> Text:
    logger.info("Converting to WAVE...")
    AudioSegment.from_file(compressed_audio_file_absolute_path, "mp3").export(output_file_path, format="wav")
    logger.info("Conversion done: {}".format(output_file_path))
    return output_file_path
