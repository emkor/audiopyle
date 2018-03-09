from typing import Any, Text, Dict
from billiard.exceptions import SoftTimeLimitExceeded

from commons.services.result_store_client import ResultApiClient
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
    mp3_file_store = LzmaJsonFileStore(AUDIO_FILES_DIR, extension="mp3")
    result_api_client = ResultApiClient("coordinator", 8080, logger)
    extraction_service = FeatureExtractionService(result_store_client=result_api_client,
                                                  audio_file_store=mp3_file_store,
                                                  logger=logger)
    try:
        extraction_service.extract_feature_and_store(request)
        return extraction_request
    except SoftTimeLimitExceeded as e:
        logger.exception(e)
        raise e
