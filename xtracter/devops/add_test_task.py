from commons.utils.constant import B2_TEST_FILE_PATH

from commons.model.remote_file_meta import RemoteFileMeta
from commons.provider.redis_queue_client import RedisQueueClient

print("Adding test file to redis queue...")
redis_client = RedisQueueClient("xtracter_tasks")
remote_audio_test_file = RemoteFileMeta(B2_TEST_FILE_PATH, 0, 0)
redis_client.add(remote_audio_test_file)
print("Added successfully!")
