from typing import Text, List, Optional

from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from pydub import AudioSegment

from commons.audio.audio_tag import Id3Tag
from commons.audio.segment_providing import read_audio_file_meta, read_segment
from commons.services.extraction import extract_features
from commons.utils.conversion import object_size_humanized
from commons.utils.env_var import get_environment_variable
from commons.utils.file_system import extract_extension
from commons.utils.logger import get_logger
from commons.vampy.feature import VampyFeatureMeta
from commons.vampy.plugin_providing import list_vampy_plugins

logger = get_logger()


def convert_if_needed(audio_file_absolute_path: Text) -> Text:
    audio_file_extension = extract_extension(audio_file_absolute_path)
    if audio_file_extension.lower() != "wav":
        logger.info("Converting to WAVE...")
        output_file_name = "{}.{}".format(audio_file_absolute_path, "wav")
        AudioSegment.from_file(audio_file_absolute_path, audio_file_extension).export(
            output_file_name, format="wav")
        logger.info("Conversion done: {}".format(output_file_name))
        return output_file_name
    else:
        logger.info("No need for file {} conversion".format(audio_file_absolute_path))
        return audio_file_absolute_path


def extract_features_with_all_plugins(output_file_name: Text) -> List[VampyFeatureMeta]:
    logger.info("Preparing for feature extraction of file {}...".format(output_file_name))
    audio_segment = read_segment(read_audio_file_meta(output_file_name))
    blacklisted_plugins = get_environment_variable(variable_name="BLACKLISTED_PLUGINS", expected_type=str,
                                                   default="").split(",")
    if blacklisted_plugins:
        logger.info("Omitting blacklisted plugins ({}): {}...".format(len(blacklisted_plugins), blacklisted_plugins))
    plugins = list_vampy_plugins(blacklisted_plugins)
    features = []
    for plugin in plugins:
        for plugin_output in plugin.outputs:
            try:
                logger.info("Extracting {}: {} from {} ({})...".format(plugin.name, plugin_output,
                                                                       audio_segment.source_file_meta.file_name,
                                                                       audio_segment.size_humanized()))
                feature = extract_features(audio_segment, plugin, plugin_output)
                logger.info(
                    "Extracted {}: {} with size of {}!".format(plugin.name, plugin_output,
                                                               object_size_humanized(feature)))
                features.append(feature)
            except Exception as e:
                logger.error("Error on plugin: {}-{}: {}".format(plugin, plugin_output, e))
    logger.info("Done feature extraction from file {}".format(output_file_name))
    return features


def read_id3_tag(input_audio_file_absolute_path: Text) -> Optional[Id3Tag]:
    try:
        audio_tags = EasyID3(input_audio_file_absolute_path)
        id3_tag = Id3Tag.from_easy_id3_object(audio_tags)
        logger.info("Tags extracted from {}: {}".format(input_audio_file_absolute_path, id3_tag))
        return id3_tag
    except ID3NoHeaderError as e:
        logger.warning("File {} does not contain ID3 tag: {}".format(input_audio_file_absolute_path, e))
        return None
