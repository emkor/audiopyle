from typing import Text, Optional

from pydub import AudioSegment

from commons.utils.file_system import TMP_DIR, file_exists, concatenate_paths
from commons.utils.logger import get_logger

logger = get_logger()


def generate_output_wav_file_path(task_id: Text) -> Text:
    return "{}.wav".format(concatenate_paths(TMP_DIR, task_id))


def convert_to_wav(compressed_audio_file_absolute_path: Text, output_file_path: Text) -> Optional[Text]:
    if file_exists(compressed_audio_file_absolute_path):
        logger.info("Converting {} to WAVE: {}...".format(compressed_audio_file_absolute_path, output_file_path))
        AudioSegment.from_file(compressed_audio_file_absolute_path, "mp3").export(output_file_path, format="wav")
        logger.info("Conversion done: {}".format(output_file_path))
        return output_file_path
    else:
        return None
