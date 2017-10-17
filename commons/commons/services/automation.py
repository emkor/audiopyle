import os
from typing import Text, Optional, List

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from pydub import AudioSegment

from commons.audio.audio_tag import Id3Tag
from commons.services.extraction import ExtractionRequest
from commons.utils.env_var import get_environment_variable
from commons.utils.file_system import extract_extension, copy_file, TMP_DIR, list_files, AUDIO_FILES_DIR
from commons.utils.logger import get_logger
from commons.vampy.plugin import VampyPlugin
from commons.vampy.plugin_providing import list_vampy_plugins

logger = get_logger()

ACCEPTED_EXTENSIONS = ("mp3", "wav", "flac")


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


def generate_extraction_requests(audio_file_names: List[Text], plugins: List[VampyPlugin]) -> List[ExtractionRequest]:
    extraction_requests = []
    for audio_file_name in audio_file_names:
        for plugin in plugins:
            for plugin_output in plugin.outputs:
                extraction_requests.append(
                    ExtractionRequest(audio_file_name=audio_file_name, plugin_key=plugin.key,
                                      plugin_output=plugin_output))
    return extraction_requests


def allowed_audio_files():
    all_file_names = list_files(AUDIO_FILES_DIR)
    audio_file_names = [f for f in all_file_names if extract_extension(f).lower() in ACCEPTED_EXTENSIONS]
    if len(audio_file_names) != len(all_file_names):
        logger.warning("Omitted {} audio files because invalid extensions (accepted ones: {})".format(
            len(all_file_names) - len(audio_file_names), ACCEPTED_EXTENSIONS))
    logger.info("Found audio file names: {}".format(audio_file_names))
    return audio_file_names


def whitelisted_plugins() -> List[VampyPlugin]:
    blacklisted_plugins = get_environment_variable(variable_name="BLACKLISTED_PLUGINS", expected_type=str,
                                                   default="").split(",")
    if blacklisted_plugins:
        logger.warning(
            "Omitting blacklisted plugins ({}): {}...".format(len(blacklisted_plugins), blacklisted_plugins))
    plugins = list_vampy_plugins(blacklisted_plugins)
    return plugins
