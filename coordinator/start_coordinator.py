from coordinator.service.b2_coordinator import B2Coordinator
from commons.provider.redis_queue_client import RedisQueueClient
from commons.utils.logging_setup import get_logger


TASK_QUEUE_NAME = "xtracter_tasks"

logger = get_logger()

redis_queue_client = RedisQueueClient(TASK_QUEUE_NAME)

logger.info("Starting coordinator pushing to {}...".format(TASK_QUEUE_NAME))
coordinator = B2Coordinator(redis_queue_client=redis_queue_client)
coordinator.get_and_push_file_list_loop()
