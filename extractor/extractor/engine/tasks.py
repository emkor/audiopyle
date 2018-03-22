from typing import Any, Text, Dict
from billiard.exceptions import SoftTimeLimitExceeded

from commons.db.session import SessionProvider
from commons.repository.audio_file import AudioFileRepository
from commons.repository.audio_tag import AudioTagRepository
from commons.repository.feature_data import FeatureDataRepository
from commons.repository.feature_meta import FeatureMetaRepository
from commons.repository.result import ResultRepository, ResultStatsRepository
from commons.repository.vampy_plugin import VampyPluginRepository, PluginConfigRepository
from commons.services.plugin_providing import VampyPluginProvider
from commons.utils.file_system import AUDIO_FILES_DIR
from commons.utils.logger import get_logger
from commons.models.extraction_request import ExtractionRequest
from commons.services.store_provider import LzmaJsonFileStore
from extractor.engine.celery import get_celery
from extractor.extraction_service import FeatureExtractionService

celery_app = get_celery()


@celery_app.task
def extract_feature(extraction_request: Dict[Text, Any]) -> Dict[Text, Any]:
    logger = get_logger()
    request = ExtractionRequest.from_serializable(extraction_request)

    plugin_provider = VampyPluginProvider(plugin_black_list=[], logger=logger)
    mp3_file_store = LzmaJsonFileStore(AUDIO_FILES_DIR, extension="mp3")

    db_session_provider = SessionProvider()
    audio_tag_repo = AudioTagRepository(db_session_provider)
    audio_meta_repo = AudioFileRepository(db_session_provider)
    plugin_repo = VampyPluginRepository(db_session_provider)
    plugin_config_repo = PluginConfigRepository(db_session_provider)
    feature_data_repo = FeatureDataRepository(db_session_provider)
    feature_meta_repo = FeatureMetaRepository(db_session_provider)
    result_repo = ResultRepository(db_session_provider, audio_meta_repo, audio_tag_repo, plugin_repo)
    result_stats_repo = ResultStatsRepository(db_session_provider)

    extraction_service = FeatureExtractionService(plugin_provider=plugin_provider,
                                                  audio_file_store=mp3_file_store,
                                                  audio_tag_repo=audio_tag_repo,
                                                  audio_meta_repo=audio_meta_repo,
                                                  plugin_repo=plugin_repo,
                                                  plugin_config_repo=plugin_config_repo,
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
