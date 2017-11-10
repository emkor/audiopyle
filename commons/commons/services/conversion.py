import os
from typing import Text
from pydub import AudioSegment
from commons.utils.file_system import extract_extension, copy_file, TMP_DIR
from commons.utils.logger import get_logger

logger = get_logger()


def copy_or_convert(audio_file_absolute_path: Text, output_file_path: Text) -> Text:
    audio_file_extension = extract_extension(audio_file_absolute_path)
    if audio_file_extension != "wav":
        output_file_path = "{}.{}".format(os.path.join(TMP_DIR, output_file_path), "wav")
        logger.info("Converting to WAVE...")
        AudioSegment.from_file(audio_file_absolute_path, audio_file_extension).export(output_file_path, format="wav")
        logger.info("Conversion done: {}".format(output_file_path))
    else:
        output_file_path = "{}.{}".format(os.path.join(TMP_DIR, output_file_path), audio_file_extension)
        logger.info(
            "No need for file {} conversion, copying to {}...".format(audio_file_absolute_path, audio_file_extension))
        copy_file(source=audio_file_absolute_path, destination=output_file_path)
        logger.info("Copied {} -> {}!".format(audio_file_absolute_path, output_file_path))
    return output_file_path
