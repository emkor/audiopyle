from commons.utils.constant import AudiopyleConst
from commons.utils.logging_setup import get_logger

from commons.model.remote_file_meta import RemoteFileMeta
from commons.provider.redis_queue_client import RedisQueueClient

logger = get_logger()

logger.info("Adding test file to redis queue...")
redis_client = RedisQueueClient("xtracter_tasks")
remote_audio_test_file = RemoteFileMeta(AudiopyleConst.B2_TEST_FILE_PATH, 0, 0)
redis_client.add(remote_audio_test_file)
logger.info("Added successfully!")
