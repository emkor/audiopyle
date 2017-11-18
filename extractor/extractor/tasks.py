from typing import Any, Text, Dict

import os
from billiard.exceptions import SoftTimeLimitExceeded

from commons.services.audio_tag_providing import read_id3_tag
from commons.services.audio_conversion import convert_to_wav, generate_output_wav_file_path
from commons.services.feature_extraction import extract_features, ExtractionRequest
from commons.services.file_meta_providing import read_wav_file_meta
from commons.services.plugin_providing import build_plugin_from_key
from commons.services.segment_providing import read_wav_segment
from commons.services.uuid_generation import generate_uuid
from commons.utils.file_system import AUDIO_FILES_DIR, remove_file
from commons.utils.logger import get_logger
from extractor.celery import app


@app.task
def extract_feature(extraction_request: Dict[Text, Any]) -> Dict[Text, Any]:
    logger = get_logger()
    task_id = generate_uuid(extraction_request)
    request = ExtractionRequest.deserialize(extraction_request)
    logger.info("Building context for extraction {}: {}...".format(task_id, request))
    audio_file_absolute_path = os.path.join(AUDIO_FILES_DIR, request.audio_file_name)
    id3_tag = read_id3_tag(audio_file_absolute_path)
    tmp_audio_file_name = convert_to_wav(audio_file_absolute_path, generate_output_wav_file_path(task_id))
    audio_file_meta = read_wav_file_meta(tmp_audio_file_name)
    audio_segment = read_wav_segment(audio_file_meta)
    plugin = build_plugin_from_key(str(request.plugin_key))
    logger.info("Built extraction context: {} {} {}".format(audio_segment, plugin, request.plugin_output))
    logger.info("Starting feature extraction...")
    try:
        feature = extract_features(audio_segment, plugin, request.plugin_output)
        logger.info("Extracted {} feature!".format(feature.__class__.__name__))
        if tmp_audio_file_name != audio_file_absolute_path:
            logger.info("Removing temporary file: {}...".format(tmp_audio_file_name))
            remove_file(tmp_audio_file_name)
            logger.info("Removed temporary file: {}!".format(tmp_audio_file_name))
        return feature.serialize()
    except SoftTimeLimitExceeded as e:
        logger.exception(e)
        if tmp_audio_file_name != audio_file_absolute_path:
            logger.info("Removing temporary file: {}...".format(tmp_audio_file_name))
            remove_file(tmp_audio_file_name)
            logger.info("Removed temporary file: {}!".format(tmp_audio_file_name))
        raise e
