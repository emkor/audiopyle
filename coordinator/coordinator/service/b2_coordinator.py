from time import sleep

from commons.model.analysis_task import AnalysisTask
from commons.model.remote_file_meta import RemoteFileMeta
from commons.model.remote_file_source import create_b2_source_config
from commons.provider.b2_audio_provider import B2AudioProvider
from commons.provider.redis_queue_client import RedisQueueClient
from commons.service.os_env_accessor import OsEnvAccessor
from commons.utils.constant import B2_ACCOUNT_ID, B2_APPLICATION_KEY, B2_RESOURCES_BUCKET, PROJECT_HOME_ENV

DEFAULT_QUEUE_NAME = 'RedisClientTestQueue'
QUEUE_RELOAD_DELAY = 5


class B2Coordinator(object):
    def __init__(self, audio_provider=None, redis_queue_client=None):
        self.b2_source_config = create_b2_source_config(B2_ACCOUNT_ID,
                                         B2_APPLICATION_KEY,
                                         B2_RESOURCES_BUCKET)
        self.audio_provider = audio_provider or B2AudioProvider(OsEnvAccessor.get_env_variable(PROJECT_HOME_ENV))
        self.redis_queue_client = redis_queue_client or RedisQueueClient(DEFAULT_QUEUE_NAME)

    def get_and_push_file_list_loop(self):
        last_timestamp = 0
        while True:
            remote_files = self.get_remote_audio_files()
            last_timestamp = self.push_file_list_to_redis(remote_files, last_timestamp)
            sleep(QUEUE_RELOAD_DELAY)

    def get_remote_audio_files(self):
        file_infos = self.audio_provider.get_raw_file_infos(self.b2_source_config)
        audio_file_infos = self._filter_audio_files(file_infos)
        audio_file_infos.sort(key=lambda k: k[u'uploadTimestamp'])

        remote_audio_files = []
        for file in audio_file_infos:
            remote_audio_files.append(RemoteFileMeta.from_dict(file))

        return remote_audio_files

    def push_file_list_to_redis(self, remote_files, last_timestamp):
        for remote_file in remote_files:
            if remote_file and remote_file.upload_timestamp > last_timestamp:
                task = AnalysisTask(remote_file, self.b2_source_config)
                self.redis_queue_client.add(task.to_dict())
                last_timestamp = remote_file.upload_timestamp
                print("Pushing to {}".format(self.redis_queue_client.queue_name))
            return last_timestamp

    def _filter_audio_files(self, files):
        return [{u'fileName': file[u'fileName'],
                 u'size': file[u'size'],
                 u'uploadTimestamp': file[u'uploadTimestamp']}
                for file in files
                if u'audio' in file[u'contentType']]
