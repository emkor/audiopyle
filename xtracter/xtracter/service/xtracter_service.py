from datetime import datetime
from time import sleep

from commons.utils.constant import AudiopyleConst

from commons.model.remote_file_meta import RemoteFileMeta
from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor
from xtracter.utils.xtracter_const import XtracterConst
from commons.commons.utils.logging_setup import myGetLogger

SLEEP_TIME_SEC = 3


class Xtracter(object):
    def __init__(self, feature_extractor, audio_meta_provider, b2_client, redis_task_client, redis_results_client):
        self.feature_extractor = feature_extractor
        self.b2_client = b2_client
        self.audio_meta_provider = audio_meta_provider
        self.redis_task_client = redis_task_client
        self.redis_results_client = redis_results_client
        self.logger = myGetLogger()

    def init(self):
        while True:
            task_dict_or_none = self.redis_task_client.take()
            if task_dict_or_none is not None:
                local_file_meta = self._download_file(task_dict_or_none)
                audio_features = self._extract_features(local_file_meta)
                # self._send_to_redis(audio_features)
                self._remove_file(local_file_meta)
            else:
                sleep(SLEEP_TIME_SEC)

    def _download_file(self, task_dict_or_none):
        start_time = datetime.utcnow()
        self.logger.info("{} received task: {}".format(start_time, task_dict_or_none))
        remote_file_meta = RemoteFileMeta.from_dict(task_dict_or_none)
        self.logger.info("Starting download of file: {}...".format(remote_file_meta))
        local_file_path = self.b2_client.download(remote_file_meta.name)
        local_file_meta = self.audio_meta_provider.read_meta_from(local_file_path)
        download_took = (datetime.utcnow() - start_time).total_seconds()
        self.logger.info("Ended downloading file: {}. Download took: {} seconds".format(local_file_meta, download_took))
        return local_file_meta

    def _extract_features(self, local_file_meta):
        start_time = datetime.utcnow()
        self.logger.info("{} starting feature extraction...".format(start_time))
        audio_features = self.feature_extractor.extract(local_file_meta)
        extraction_took = (datetime.utcnow() - start_time).total_seconds()
        self.logger.info("Extracted {} features in {} seconds.".format(len(audio_features), extraction_took))
        return audio_features

    def _send_to_redis(self, audio_features):
        start_time = datetime.utcnow()
        self.logger.info("{} exporting {} features to redis results queue...".format(start_time, len(audio_features)))
        for audio_feature in audio_features:
            self.redis_results_client.add(audio_feature)
        sending_took = (datetime.utcnow() - start_time).total_seconds()
        self.logger.info("Ended exporting results in {} seconds.".format(sending_took))

    def _remove_file(self, local_file_meta):
        home = OsEnvAccessor.get_env_variable(AudiopyleConst.PROJECT_HOME_ENV)
        file_path = FileAccessor.join(home, XtracterConst.AUDIO_FILES_CACHE_PATH, local_file_meta.filename)
        if FileAccessor.exists(file_path):
            FileAccessor.remove_file(file_path)
            self.logger.info("Removed file: {}".format(file_path))
        else:
            self.logger.warning("Could not remove file: {}".format(file_path))
