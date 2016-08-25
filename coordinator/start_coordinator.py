import logging

from coordinator.service.b2_coordinator import B2Coordinator
from commons.provider.redis_queue_client import RedisQueueClient


TASK_QUEUE_NAME = "xtracter_tasks"
COORDINATOR_LOGGER_NAME = "coordinator"
COMMONS_LOGGER_NAME = "commons"

handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)s | %(asctime)s | %(levelname)s | %(funcName)s | %(message)s')
handler.setFormatter(formatter)

coordinator_logger = logging.getLogger(COORDINATOR_LOGGER_NAME)
coordinator_logger.setLevel(logging.INFO)
coordinator_logger.addHandler(handler)

commons_logger = logging.getLogger(COMMONS_LOGGER_NAME)
commons_logger.setLevel(logging.INFO)
commons_logger.addHandler(handler)

redis_queue_client = RedisQueueClient(TASK_QUEUE_NAME)

coordinator_logger.info("Starting coordinator pushing to {}...".format(TASK_QUEUE_NAME))
coordinator = B2Coordinator(redis_queue_client=redis_queue_client)
coordinator.get_and_push_file_list_loop()
