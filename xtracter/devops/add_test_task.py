import logging

from commons.utils.constant import AudiopyleConst

from commons.model.remote_file_meta import RemoteFileMeta
from commons.provider.redis_queue_client import RedisQueueClient

logger = logging.getLogger(__name__)
# logger = logging.getLogger("xtracter")
# logger.setLevel(logging.INFO)
# handler = logging.StreamHandler()
# handler.setLevel(logging.INFO)
# formatter = logging.Formatter('%(name)s | %(asctime)s | %(levelname)s | %(funcName)s | %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

logger.info("Adding test file to redis queue...")
redis_client = RedisQueueClient("xtracter_tasks")
remote_audio_test_file = RemoteFileMeta(AudiopyleConst.B2_TEST_FILE_PATH, 0, 0)
redis_client.add(remote_audio_test_file)
logger.info("Added successfully!")
