from logging import Logger
from typing import Any, Text, Dict

from billiard.exceptions import SoftTimeLimitExceeded
from datetime import datetime

from commons.models.extraction_request import ExtractionRequest
from commons.models.result import AnalysisResult, ResultVersion, AnalysisStats
from commons.services.audio_tag_providing import read_id3_tag
from commons.services.audio_conversion import convert_to_wav, generate_output_wav_file_path
from commons.services.feature_extraction import extract_features
from commons.services.feature_meta_extraction import get_feature_meta
from commons.services.file_meta_providing import read_wav_file_meta, read_file_meta, read_mp3_file_meta
from commons.services.plugin_providing import build_plugin_from_key
from commons.services.segment_providing import read_wav_segment
from commons.services.store_provider import JsonFileStore
from commons.services.uuid_generation import generate_uuid
from commons.utils.conversion import seconds_between
from commons.utils.file_system import AUDIO_FILES_DIR, remove_file, concatenate_paths, RESULTS_DIR
from commons.utils.logger import get_logger
from extractor.celery import app


@app.task
def extract_feature(extraction_request: Dict[Text, Any]) -> Dict[Text, Any]:
    task_start_time = datetime.utcnow()
    logger = get_logger()
    task_id = generate_uuid(extraction_request)
    request = ExtractionRequest.from_serializable(extraction_request)
    logger.info("Building context for extraction {}: {}...".format(task_id, request))
    file_store = JsonFileStore(RESULTS_DIR)
    audio_file_absolute_path = concatenate_paths(AUDIO_FILES_DIR, request.audio_file_name)
    input_file_meta = read_file_meta(audio_file_absolute_path)
    input_audio_meta = read_mp3_file_meta(audio_file_absolute_path)
    id3_tag = read_id3_tag(audio_file_absolute_path)

    conversion_start_time = datetime.utcnow()
    tmp_audio_file_name = convert_to_wav(audio_file_absolute_path, generate_output_wav_file_path(task_id))
    conversion_time = seconds_between(conversion_start_time)

    wav_audio_meta = read_wav_file_meta(tmp_audio_file_name)
    wav_data = read_wav_segment(wav_audio_meta)
    plugin = build_plugin_from_key(str(request.plugin_key))
    logger.debug("Built extraction context: {} {}! Extracting features...".format(plugin, request.plugin_output))
    try:
        extraction_start_time = datetime.utcnow()
        feature = extract_features(wav_data, wav_audio_meta, plugin, request.plugin_output)
        extraction_time = seconds_between(extraction_start_time)

        feature_store_start_time = datetime.utcnow()
        file_store.store("{}-data".format(task_id), feature.to_serializable())
        feature_store_time = seconds_between(feature_store_start_time)

        _remove_wav_file(audio_file_absolute_path, tmp_audio_file_name, logger)

        analysis_result_build_start_time = datetime.utcnow()
        feature_meta = get_feature_meta(feature, plugin, request.plugin_output)
        analysis_result = AnalysisResult(ResultVersion.V1, task_id, input_file_meta, input_audio_meta, wav_audio_meta,
                                         id3_tag, feature_meta)
        file_store.store("{}-meta".format(task_id), analysis_result.to_serializable())
        analysis_result_build_time = seconds_between(analysis_result_build_start_time)

        task_time = seconds_between(task_start_time)
        analysis_stats = AnalysisStats(task_time, conversion_time, extraction_time, feature_store_time,
                                       analysis_result_build_time)
        file_store.store("{}-stats".format(task_id), analysis_stats.to_serializable())
        return extraction_request
    except SoftTimeLimitExceeded as e:
        logger.exception(e)
        _remove_wav_file(audio_file_absolute_path, tmp_audio_file_name, logger)
        raise e


def _remove_wav_file(audio_file_absolute_path, tmp_audio_file_name, logger):
    # type: (Text, Text, Logger) -> None
    if tmp_audio_file_name != audio_file_absolute_path:
        logger.debug("Removing temporary file: {}...".format(tmp_audio_file_name))
        remove_file(tmp_audio_file_name)
        logger.debug("Removed temporary file: {}!".format(tmp_audio_file_name))
