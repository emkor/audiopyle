from logging import Logger
from typing import Text, Tuple, Optional
from datetime import datetime

import numpy

from commons.services.result_store_client import ResultApiClient
from commons.utils.conversion import seconds_between
from commons.models.audio_tag import Id3Tag
from commons.models.extraction_request import ExtractionRequest
from commons.models.feature import VampyFeatureAbstraction
from commons.models.file_meta import FileMeta, Mp3AudioFileMeta, AudioFileMeta
from commons.models.plugin import VampyPlugin
from commons.models.result import AnalysisResult, AnalysisStats
from commons.services.audio_tag_providing import read_id3_tag
from commons.services.feature_extraction import extract_raw_feature, build_feature_object
from commons.services.feature_meta_extraction import build_feature_meta
from commons.services.file_meta_providing import read_file_meta, read_mp3_file_meta
from commons.services.plugin_providing import build_plugin_from_key
from commons.services.segment_providing import read_raw_audio_from_mp3
from commons.services.store_provider import FileStore


class FeatureExtractionService(object):
    def __init__(self, result_store_client: ResultApiClient, audio_file_store: FileStore, logger: Logger) -> None:
        self.result_store_client = result_store_client
        self.audio_file_store = audio_file_store
        self.logger = logger
        self._temporary_wav_file = None  # type: Optional[Text]

    def extract_feature_and_store(self, request: ExtractionRequest):
        task_start_time = datetime.utcnow()
        task_id = request.uuid()
        self.logger.info("Building context for extraction {}: {}...".format(task_id, request))
        input_audio_file_path = self.audio_file_store.get_full_path(request.audio_file_identifier)
        plugin = build_plugin_from_key(str(request.plugin_key))
        file_meta, audio_meta, id3_tag, read_input_file_time = self._read_file_meta(input_audio_file_path)
        wav_data, read_raw_audio_time = self._read_raw_audio_data_from_mp3(input_audio_file_path)
        self.logger.debug("Built context: {} {}! Extracting features...".format(plugin.key, request.plugin_output))
        feature_object, extraction_time = self._do_extraction(task_id, plugin, request.plugin_output,
                                                              audio_meta, wav_data)
        feature_store_time = self._store_feature_data(feature_object, task_id)
        analysis_result, result_build_time = self._build_analysis_result(audio_meta, feature_object, file_meta,
                                                                         id3_tag, request.plugin_output, task_id)
        result_store_time = self._store_analysis_result(analysis_result, task_id)
        task_time = seconds_between(task_start_time)
        self._store_analysis_stats(task_id, extraction_time, feature_store_time, result_build_time,
                                   result_store_time, task_time, read_input_file_time, read_raw_audio_time)

    def _store_analysis_stats(self, task_id: Text, extraction_time: float, feature_store_time: float,
                              result_build_time: float, result_store_time: float, task_time: float,
                              read_input_file_time, read_raw_audio_time) -> None:
        analysis_stats = AnalysisStats(task_time, extraction_time, feature_store_time,
                                       result_build_time, result_store_time, read_input_file_time, read_raw_audio_time)
        self.result_store_client.store_stats(task_id, analysis_stats.to_serializable())

    def _store_analysis_result(self, analysis_result: AnalysisResult, task_id: Text) -> float:
        result_store_start_time = datetime.utcnow()
        self.result_store_client.store_meta(task_id, analysis_result.to_serializable())
        result_store_time = seconds_between(result_store_start_time)
        return result_store_time

    def _build_analysis_result(self, audio_meta: Mp3AudioFileMeta, feature: VampyFeatureAbstraction,
                               file_meta: FileMeta, id3_tag: Id3Tag, plugin_output: Text,
                               task_id: Text) -> Tuple[AnalysisResult, float]:
        analysis_result_build_start_time = datetime.utcnow()
        feature_meta = build_feature_meta(task_id, feature, plugin_output)
        analysis_result = AnalysisResult(task_id, file_meta, audio_meta, id3_tag, feature_meta)
        return analysis_result, seconds_between(analysis_result_build_start_time)

    def _store_feature_data(self, feature, task_id):
        feature_store_start_time = datetime.utcnow()
        self.result_store_client.store_data(task_id, feature.to_serializable())
        feature_store_time = seconds_between(feature_store_start_time)
        return feature_store_time

    def _do_extraction(self, task_id: str, plugin: VampyPlugin, plugin_output: Text, input_audio_meta: AudioFileMeta,
                       wav_data: numpy.ndarray) -> Tuple[VampyFeatureAbstraction, float]:
        extraction_start_time = datetime.utcnow()
        raw_feature = extract_raw_feature(wav_data, input_audio_meta.sample_rate, plugin.key, plugin_output)
        feature_object = build_feature_object(task_id=task_id, extracted_data=raw_feature)
        extraction_time = seconds_between(extraction_start_time)
        return feature_object, extraction_time

    def _read_raw_audio_data_from_mp3(self, input_file_path: Text) -> Tuple[numpy.ndarray, float]:
        read_raw_audio_start_time = datetime.utcnow()
        raw_data = read_raw_audio_from_mp3(input_file_path)
        read_raw_audio_time = seconds_between(read_raw_audio_start_time)
        return raw_data, read_raw_audio_time

    def _read_file_meta(self, audio_file_absolute_path: Text) -> Tuple[FileMeta, Mp3AudioFileMeta, Id3Tag, float]:
        read_input_file_start_time = datetime.utcnow()
        input_file_meta = read_file_meta(audio_file_absolute_path)
        input_audio_meta = read_mp3_file_meta(audio_file_absolute_path)
        id3_tag = read_id3_tag(audio_file_absolute_path)
        read_input_file_time = seconds_between(read_input_file_start_time)
        return input_file_meta, input_audio_meta, id3_tag, read_input_file_time
