from logging import Logger
from typing import Any, Text, Dict

from billiard.exceptions import SoftTimeLimitExceeded

from commons.models.result import AnalysisResult, ResultVersion
from commons.services.audio_tag_providing import read_id3_tag
from commons.services.audio_conversion import convert_to_wav, generate_output_wav_file_path
from commons.services.feature_extraction import extract_features, ExtractionRequest, get_feature_meta
from commons.services.file_meta_providing import read_wav_file_meta, read_file_meta, read_mp3_file_meta
from commons.services.plugin_providing import build_plugin_from_key
from commons.services.segment_providing import read_wav_segment
from commons.services.uuid_generation import generate_uuid
from commons.utils.file_system import AUDIO_FILES_DIR, remove_file, concatenate_paths, store_result_as_json
from commons.utils.logger import get_logger
from extractor.celery import app


@app.task
def extract_feature(extraction_request: Dict[Text, Any]) -> Dict[Text, Any]:
    logger = get_logger()
    task_id = generate_uuid(extraction_request)
    request = ExtractionRequest.from_serializable(extraction_request)
    logger.info("Building context for extraction {}: {}...".format(task_id, request))
    audio_file_absolute_path = concatenate_paths(AUDIO_FILES_DIR, request.audio_file_name)
    input_file_meta = read_file_meta(audio_file_absolute_path)
    input_audio_meta = read_mp3_file_meta(audio_file_absolute_path)
    id3_tag = read_id3_tag(audio_file_absolute_path)
    tmp_audio_file_name = convert_to_wav(audio_file_absolute_path, generate_output_wav_file_path(task_id))
    temp_audio_meta = read_wav_file_meta(tmp_audio_file_name)
    audio_segment = read_wav_segment(audio_file_absolute_path, temp_audio_meta)
    plugin = build_plugin_from_key(str(request.plugin_key))
    logger.info("Built extraction context: {} {} {}".format(audio_segment, plugin, request.plugin_output))
    logger.info("Starting feature extraction...")
    try:
        feature = extract_features(audio_segment, plugin, request.plugin_output)
        logger.info("Extracted {} feature!".format(feature.__class__.__name__))
        _remove_wav_file(audio_file_absolute_path, tmp_audio_file_name, logger)
        analysis_result = AnalysisResult(ResultVersion.V1, task_id, input_file_meta, input_audio_meta, temp_audio_meta,
                                         id3_tag, get_feature_meta(feature))
        analysis_result_serializable = _store_results_as_files(analysis_result, feature, task_id)
        return analysis_result_serializable
    except SoftTimeLimitExceeded as e:
        logger.exception(e)
        _remove_wav_file(audio_file_absolute_path, tmp_audio_file_name, logger)
        raise e


def _store_results_as_files(analysis_result, feature, task_id):
    analysis_result_serializable = analysis_result.to_serializable()
    store_result_as_json(analysis_result_serializable, task_id, "meta")
    store_result_as_json(feature.to_serializable(), task_id, "data")
    return analysis_result_serializable


def _remove_wav_file(audio_file_absolute_path, tmp_audio_file_name, logger):
    # type: (Text, Text, Logger) -> None
    if tmp_audio_file_name != audio_file_absolute_path:
        logger.info("Removing temporary file: {}...".format(tmp_audio_file_name))
        remove_file(tmp_audio_file_name)
        logger.info("Removed temporary file: {}!".format(tmp_audio_file_name))
