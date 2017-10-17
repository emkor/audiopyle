import os
from typing import Text, Optional

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from pydub import AudioSegment

from commons.audio.audio_tag import Id3Tag
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


def read_id3_tag(input_audio_file_absolute_path: Text) -> Optional[Id3Tag]:
    try:
        audio_tags = EasyID3(input_audio_file_absolute_path)
        id3_tag = Id3Tag.from_easy_id3_object(audio_tags)
        logger.info("Tags extracted from {}: {}".format(input_audio_file_absolute_path, id3_tag))
        return id3_tag
    except ID3NoHeaderError as e:
        logger.warning("File {} does not contain ID3 tag: {}".format(input_audio_file_absolute_path, e))
        return None
