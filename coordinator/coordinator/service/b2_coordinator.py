import logging
from time import sleep

from commons.model.b2_config import B2Config
from commons.model.remote_file_meta import RemoteFileMeta
from commons.provider.b2_audio_provider import B2AudioProvider
from commons.provider.redis_queue_client import RedisQueueClient
from commons.service.os_env_accessor import OsEnvAccessor
from commons.utils.constant import AudiopyleConst

DEFAULT_QUEUE_NAME = 'RedisClientTestQueue'
QUEUE_RELOAD_DELAY = 5


class B2Coordinator(object):
    def __init__(self, audio_provider=None, redis_queue_client=None):
        if(audio_provider is not None):
            self.audio_provider = audio_provider
        else:
            self.audio_provider = B2AudioProvider(
                B2Config(AudiopyleConst.B2_ACCOUNT_ID,
                         AudiopyleConst.B2_APPLICATION_KEY,
                         AudiopyleConst.B2_RESOURCES_BUCKET),
                OsEnvAccessor.get_env_variable(
                    AudiopyleConst.PROJECT_HOME_ENV))

        self.redis_queue_client = redis_queue_client \
            or RedisQueueClient(DEFAULT_QUEUE_NAME)

        self.logger = logging.getLogger(__name__)

    def get_remote_audio_files(self):
        file_infos = self.audio_provider.get_file_infos()
        audio_file_infos = self._filter_audio_files(file_infos)
        audio_file_infos.sort(key=lambda k: k[u'uploadTimestamp'])

        remote_audio_files = []
        for file in audio_file_infos:
            remote_audio_files.append(RemoteFileMeta.from_dict(file))

        return remote_audio_files

    def get_and_push_file_list_loop(self):
        last_timestamp = 0
        while (True):
            files = self.get_remote_audio_files()
            last_timestamp = self.push_file_list_to_redis(files, last_timestamp)
            sleep(QUEUE_RELOAD_DELAY)

    def push_file_list_to_redis(self, files, last_timestamp):
        for file in files:
            if (file and file.upload_timestamp > last_timestamp):
                self.redis_queue_client.add(file)
                last_timestamp = file.upload_timestamp
                self.logger.info("Pushing {} to {}".format(
                    file, self.redis_queue_client.queue_name))
        return last_timestamp

    def _filter_audio_files(self, files):
        return [{u'fileName': file[u'fileName'],
                 u'size': file[u'size'],
                 u'uploadTimestamp': file[u'uploadTimestamp']}
                for file in files
                if u'audio' in file[u'contentType']]
