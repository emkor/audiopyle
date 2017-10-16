import json
import os
from typing import Any, Text, Dict

from billiard.exceptions import SoftTimeLimitExceeded

from commons.audio.segment_providing import read_audio_file_meta, read_segment
from commons.services.extraction import extract_features, ExtractionRequest
from commons.services.automation import read_id3_tag, copy_or_convert
from commons.utils.file_system import AUDIO_FILES_DIR, remove_file, RESULTS_DIR
from commons.utils.logger import get_logger
from commons.vampy.plugin_providing import build_plugin_from_key
from extractor.celery import app


@app.task
def extract_feature(extraction_request: Dict[Text, Any]) -> Text:
    tmp_audio_file_name, feature_file_path = None, None
    logger = get_logger()
    request = ExtractionRequest.deserialize(extraction_request)
    task_id = request.uuid()
    logger.info("Building context for extraction {}: {}...".format(task_id, request))
    audio_file_absolute_path = os.path.join(AUDIO_FILES_DIR, request.audio_file_name)
    id3_tag = read_id3_tag(audio_file_absolute_path)
    tmp_audio_file_name = copy_or_convert(audio_file_absolute_path, task_id)
    audio_file_meta = read_audio_file_meta(tmp_audio_file_name)
    audio_segment = read_segment(audio_file_meta)
    plugin = build_plugin_from_key(str(request.plugin_key))
    logger.info("Built extraction context: {} {} {}".format(audio_segment, plugin, request.plugin_output))
    logger.info("Starting feature extraction...")
    try:
        feature = extract_features(audio_segment, plugin, request.plugin_output)
        logger.info("Extracted {} feature!".format(feature.__class__.__name__))
        feature_file_name = "{}.{}".format(task_id, "json")
        feature_file_path = os.path.join(RESULTS_DIR, feature_file_name)
        with open(feature_file_path, mode="w") as feature_file:
            json.dump(feature.serialize(), feature_file)
        logger.info("Removing temporary file: {}...".format(tmp_audio_file_name))
        remove_file(tmp_audio_file_name)
        logger.info("Removed temporary file: {}!".format(tmp_audio_file_name))
        return feature_file_name
    except SoftTimeLimitExceeded as e:
        if tmp_audio_file_name:
            logger.warning("Time's out, removing temporary file: {}...".format(tmp_audio_file_name))
            remove_file(tmp_audio_file_name)
            logger.info("Removed temporary file: {}!".format(tmp_audio_file_name))
        if feature_file_path:
            logger.warning("Time's out, removing temporary file: {}...".format(tmp_audio_file_name))
            remove_file(tmp_audio_file_name)
            logger.info("Removed temporary file: {}!".format(tmp_audio_file_name))
        raise e
