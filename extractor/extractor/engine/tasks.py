from typing import Any, Text, Dict
from billiard.exceptions import SoftTimeLimitExceeded

from commons.utils.file_system import RESULTS_DATA_DIR, RESULTS_STATS_DIR, RESULTS_META_DIR
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
    data_store = LzmaJsonFileStore(RESULTS_DATA_DIR)
    meta_store = LzmaJsonFileStore(RESULTS_META_DIR)
    stats_store = LzmaJsonFileStore(RESULTS_STATS_DIR)
    extraction_service = FeatureExtractionService(feature_data_store=data_store,
                                                  feature_meta_store=meta_store,
                                                  feature_stats_store=stats_store,
                                                  logger=logger)
    try:
        extraction_service.extract_feature_and_store(request)
        return extraction_request
    except SoftTimeLimitExceeded as e:
        logger.exception(e)
        raise e
