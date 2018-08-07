from typing import Any, Text, Dict
from billiard.exceptions import SoftTimeLimitExceeded

from audiopyle.lib.db.session import SessionProvider
from audiopyle.lib.repository.audio_file import AudioFileRepository
from audiopyle.lib.repository.audio_tag import AudioTagRepository
from audiopyle.lib.repository.feature_data import FeatureDataRepository
from audiopyle.lib.repository.feature_meta import FeatureMetaRepository
from audiopyle.lib.repository.metric import MetricDefinitionRepository, MetricValueRepository
from audiopyle.lib.repository.result import ResultRepository, ResultStatsRepository
from audiopyle.lib.repository.vampy_plugin import VampyPluginRepository, PluginConfigRepository
from audiopyle.lib.services.plugin_providing import VampyPluginProvider
from audiopyle.lib.utils.file_system import AUDIO_FILES_DIR
from audiopyle.lib.utils.logger import get_logger
from audiopyle.lib.models.extraction_request import ExtractionRequest
from audiopyle.lib.services.store_provider import Mp3FileStore
from audiopyle.worker.engine.celery import get_celery
from audiopyle.worker.extraction_service import FeatureExtractionService

celery_app = get_celery()


@celery_app.task
def extract_feature(extraction_request: Dict[Text, Any]) -> Dict[Text, Any]:
    logger = get_logger()
    request = ExtractionRequest.from_serializable(extraction_request)

    plugin_provider = VampyPluginProvider(plugin_black_list=[], logger=logger)
    mp3_file_store = Mp3FileStore(AUDIO_FILES_DIR)

    db_session_provider = SessionProvider()
    audio_tag_repo = AudioTagRepository(db_session_provider)
    audio_meta_repo = AudioFileRepository(db_session_provider)
    plugin_repo = VampyPluginRepository(db_session_provider)
    plugin_config_repo = PluginConfigRepository(db_session_provider)
    feature_data_repo = FeatureDataRepository(db_session_provider)
    feature_meta_repo = FeatureMetaRepository(db_session_provider)
    metric_definition_repo = MetricDefinitionRepository(db_session_provider, plugin_repo)
    metric_value_repo = MetricValueRepository(db_session_provider, metric_definition_repo)
    result_repo = ResultRepository(db_session_provider, audio_meta_repo, audio_tag_repo, plugin_repo,
                                   plugin_config_repo)
    result_stats_repo = ResultStatsRepository(db_session_provider)

    extraction_service = FeatureExtractionService(plugin_provider=plugin_provider,
                                                  audio_file_store=mp3_file_store,
                                                  audio_tag_repo=audio_tag_repo,
                                                  audio_meta_repo=audio_meta_repo,
                                                  plugin_repo=plugin_repo,
                                                  plugin_config_repo=plugin_config_repo,
                                                  metric_definition_repo=metric_definition_repo,
                                                  metric_value_repo=metric_value_repo,
                                                  feature_data_repo=feature_data_repo,
                                                  feature_meta_repo=feature_meta_repo,
                                                  result_repo=result_repo,
                                                  result_stats_repo=result_stats_repo,
                                                  logger=logger)
    try:
        extraction_service.extract_feature_and_store(request)
        return extraction_request
    except SoftTimeLimitExceeded as e:
        logger.exception(e)
        raise e
