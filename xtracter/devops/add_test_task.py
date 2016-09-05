from commons.model.analysis_task import AnalysisTask
from commons.model.remote_file_source import B2Config
from commons.utils.constant import B2_TEST_FILE_PATH, B2_ACCOUNT_ID, B2_APPLICATION_KEY, B2_RESOURCES_BUCKET

from commons.model.remote_file_meta import RemoteFileMeta
from commons.provider.redis_queue_client import RedisQueueClient

print("Adding test file to redis queue...")
redis_client = RedisQueueClient("xtracter_tasks")
remote_audio_test_file_meta = RemoteFileMeta(B2_TEST_FILE_PATH, 0, 0)
remote_audio_test_file_source = B2Config(B2_ACCOUNT_ID, B2_APPLICATION_KEY, B2_RESOURCES_BUCKET)
analysis_task = AnalysisTask(remote_audio_test_file_meta, remote_audio_test_file_source)
redis_client.add(analysis_task.to_dict())
print("Added successfully!")
