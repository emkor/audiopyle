import os
from typing import Any, Text, Dict

from commons.audio.segment_providing import read_audio_file_meta, read_segment
from commons.services.extraction import extract_features, ExtractionRequest
from commons.services.automation import read_id3_tag, extract_features_with_all_plugins, convert_if_needed
from commons.utils.conversion import object_size_humanized
from commons.utils.file_system import AUDIO_FILES_DIR
from commons.utils.logger import get_logger
from commons.vampy.plugin_providing import build_plugin_from_key
from extractor.celery import app

logger = get_logger()


@app.task
def extract_all_features(audio_file_name: Text) -> int:
    logger.info("Doing extract all on {}...".format(audio_file_name))
    audio_file_absolute_path = os.path.join(AUDIO_FILES_DIR, audio_file_name)
    id3_tag = read_id3_tag(audio_file_absolute_path)
    logger.info("Read file tags: {}".format(id3_tag))
    output_file_name = convert_if_needed(audio_file_absolute_path)
    features = extract_features_with_all_plugins(output_file_name)
    logger.info(
        "Done extracting all features from {}! Size: {}".format(audio_file_name, object_size_humanized(features)))
    return len(features)


@app.task
def extract_feature(extraction_request: Dict[Text, Any]) -> Dict[Text, Any]:
    request = ExtractionRequest.deserialize(extraction_request)
    logger.info("Building context for extraction: {}...".format(request))
    audio_file_absolute_path = os.path.join(AUDIO_FILES_DIR, request.audio_file_name)
    audio_file_meta = read_audio_file_meta(audio_file_absolute_path)
    audio_segment = read_segment(audio_file_meta)
    plugin = build_plugin_from_key(str(request.plugin_key))
    logger.info("Built extraction context: {} {} {}".format(audio_segment, plugin, request.plugin_output))
    logger.info("Starting feature extraction...")
    feature = extract_features(audio_segment, plugin, str(request.plugin_output))
    logger.info("Extracted {} feature!".format(feature.__class__.__name__))
    return feature.serialize()
