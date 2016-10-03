from datetime import datetime
from time import sleep

from commons.model.analysis_result import AnalysisResult
from commons.model.analysis_task import AnalysisTask
from commons.utils.constant import PROJECT_HOME_ENV
from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor
from xtracter.utils.xtracter_const import AUDIO_FILES_CACHE_PATH

SLEEP_TIME_SEC = 3


class Xtracter(object):
    def __init__(self, feature_extractor, audio_meta_provider, remote_file_provider, redis_task_client,
                 redis_results_client):
        """
        :type feature_extractor: xtracter.service.feature_extractor.FeatureExtractor
        :type audio_meta_provider: xtracter.provider.audio_meta_provider.LocalAudioMetaProvider
        :type remote_file_provider: commons.provider.b2_audio_provider.AbstractRemoteAudioProvider
        :type redis_task_client: commons.provider.redis_queue_client.RedisQueueClient
        :type redis_results_client: commons.provider.redis_queue_client.RedisQueueClient
        :rtype: xtracter.service.xtracter_service.Xtracter
        """
        self.feature_extractor = feature_extractor
        self.audio_meta_provider = audio_meta_provider
        self.remote_file_provider = remote_file_provider
        self.redis_task_client = redis_task_client
        self.redis_results_client = redis_results_client
        self.destination_path = FileAccessor.join(OsEnvAccessor.get_env_variable("AUDIOPYLE_HOME"), "xtracter",
                                                  "wav_temp")

    def init(self):
        while True:
            task_dict_or_none = self.redis_task_client.take()
            if task_dict_or_none is not None:
                analysis_task = AnalysisTask.from_dict(task_dict_or_none)
                local_file_meta = self._download_file(analysis_task)
                audio_features = self._extract_features(local_file_meta)
                analysis_result = AnalysisResult(analysis_task, audio_features)
                self._send_to_redis(analysis_result)
                self._remove_file(local_file_meta)
            else:
                sleep(SLEEP_TIME_SEC)

    def _download_file(self, analysis_task):
        start_time = datetime.utcnow()
        print("{} received task: {}".format(start_time, analysis_task))
        print("Starting downloading file: {} from: {}".format(analysis_task.remote_file_meta,
                                                              analysis_task.remote_file_source))
        local_file_path = self.remote_file_provider.download(analysis_task.remote_file_source,
                                                             analysis_task.remote_file_meta)
        local_file_meta = self.audio_meta_provider.read_meta_from(local_file_path)
        download_took = (datetime.utcnow() - start_time).total_seconds()
        print("Ended downloading file: {}. Download took: {} seconds".format(local_file_meta, download_took))
        return local_file_meta

    def _extract_features(self, local_file_meta):
        start_time = datetime.utcnow()
        print("{} starting feature extraction...".format(start_time))
        audio_features = self.feature_extractor.extract(local_file_meta)
        extraction_took = (datetime.utcnow() - start_time).total_seconds()
        print("Extracted {} features in {} seconds.".format(len(audio_features), extraction_took))
        return audio_features

    def _send_to_redis(self, analysis_result):
        start_time = datetime.utcnow()
        print("{} exporting {} features to redis results queue...".format(start_time,
                                                                          len(analysis_result.features)))
        self.redis_results_client.add(analysis_result.to_dict())
        sending_took = (datetime.utcnow() - start_time).total_seconds()
        print("Ended exporting results in {} seconds.".format(sending_took))

    def _remove_file(self, local_file_meta):
        home = OsEnvAccessor.get_env_variable(PROJECT_HOME_ENV)
        file_path = FileAccessor.join(home, "xtracter", AUDIO_FILES_CACHE_PATH, local_file_meta.filename)
        if FileAccessor.exists(file_path):
            FileAccessor.remove_file(file_path)
            print("Removed file: {}".format(file_path))
        else:
            print("Could not remove file: {}".format(file_path))
