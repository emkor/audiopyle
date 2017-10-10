from typing import Text, List, Tuple, Union, Dict, Any, Optional

import vamp
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from pydub import AudioSegment

from commons.abstractions.model import Model
from commons.audio.audio_tag import Id3Tag
from commons.audio.segment import MonoAudioSegment
from commons.audio.segment_providing import read_audio_file_meta, read_segment
from commons.utils.conversion import object_size_humanized, first_element_or, safe_cast
from commons.utils.file_system import extract_extension
from commons.utils.logger import get_logger
from commons.vampy.feature import VampyFeatureMeta, VampyVariableStepFeature, VampyConstantStepFeature
from commons.vampy.plugin import VampyPlugin
from commons.vampy.plugin_providing import list_vampy_plugins

logger = get_logger()


class ExtractionRequest(Model):
    def __init__(self, audio_file_name: Text, plugin_key: Text, plugin_output: Text) -> None:
        self.audio_file_name = audio_file_name
        self.plugin_key = plugin_key
        self.plugin_output = plugin_output


def extract_features(audio_segment: MonoAudioSegment, vampy_plugin: VampyPlugin, output_name: Text, step_size: int = 0,
                     block_size: int = 0) -> VampyFeatureMeta:
    feature_meta = VampyFeatureMeta(vampy_plugin=vampy_plugin, segment_meta=audio_segment.get_meta(),
                                    plugin_output=output_name)
    raw_results = vamp.collect(data=audio_segment.data, sample_rate=audio_segment.source_file_meta.sample_rate,
                               plugin_key=vampy_plugin.key, output=output_name, step_size=step_size,
                               block_size=block_size)
    return _map_feature(feature_meta=feature_meta, extracted_data=raw_results)


def _map_feature(feature_meta: VampyFeatureMeta, extracted_data: Dict[Text, List[Dict[str, Any]]]) -> VampyFeatureMeta:
    data_type = list(extracted_data.keys())[0]
    if data_type == "list":
        return VampyVariableStepFeature(vampy_plugin=feature_meta.vampy_plugin, segment_meta=feature_meta.segment_meta,
                                        plugin_output=feature_meta.plugin_output, value_list=extracted_data.get("list"))
    elif data_type in ("vector", "matrix"):
        data = extracted_data.get("vector") or extracted_data.get("matrix")
        return VampyConstantStepFeature(vampy_plugin=feature_meta.vampy_plugin, segment_meta=feature_meta.segment_meta,
                                        plugin_output=feature_meta.plugin_output, time_step=data[0], matrix=data[1])
    else:
        raise NotImplementedError("Can not recognize feature type: {}".format(extracted_data.keys()))


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
    plugins = list_vampy_plugins()
    features = []
    for plugin in plugins:
        for plugin_output in plugin.outputs:
            try:
                logger.info("Extracting {}: {}...".format(plugin.name, plugin_output))
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
        id3_tag = Id3Tag(artist=audio_tags["artist"], title=audio_tags["title"], album=audio_tags.get("album"),
                         date=safe_cast(first_element_or(audio_tags.get("date")), int, None),
                         track=safe_cast(first_element_or(audio_tags.get("tracknumber")), int, None),
                         genre=safe_cast(first_element_or(audio_tags.get("genre")), int, None))
        logger.info("Tags extracted from {}: {}".format(input_audio_file_absolute_path, id3_tag))
        return id3_tag
    except ID3NoHeaderError as e:
        logger.warning("File {} does not contain ID3 tag: {}".format(input_audio_file_absolute_path, e))
        return None
