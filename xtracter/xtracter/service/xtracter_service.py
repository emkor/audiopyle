from datetime import datetime
from time import sleep

from commons.model.analysis_task import AnalysisTask
from commons.provider.b2_audio_provider import B2AudioProvider
from commons.utils.constant import PROJECT_HOME_ENV

from commons.model.remote_file_meta import RemoteFileMeta
from commons.service.file_accessor import FileAccessor
from commons.service.os_env_accessor import OsEnvAccessor
from xtracter.utils.xtracter_const import AUDIO_FILES_CACHE_PATH

SLEEP_TIME_SEC = 3


class Xtracter(object):
    def __init__(self, feature_extractor, audio_meta_provider, remote_file_provider, redis_task_client,
                 redis_results_client):
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
                local_file_meta = self._download_file(task_dict_or_none)
                audio_features = self._extract_features(local_file_meta)
                self._send_to_redis(audio_features)
                self._remove_file(local_file_meta)
            else:
                sleep(SLEEP_TIME_SEC)

    def _download_file(self, task_dict_or_none):
        start_time = datetime.utcnow()
        print("{} received task: {}".format(start_time, task_dict_or_none))
        analysis_task = AnalysisTask.from_dict(task_dict_or_none)
        print("Starting downloading file: {} from: {}".format(analysis_task.remote_file_meta,
                                                              analysis_task.remote_file_source))
        b2_client = B2AudioProvider(analysis_task.remote_file_source, self.destination_path)
        local_file_path = b2_client.download(analysis_task.remote_file_source, analysis_task.remote_file_meta)
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

    def _send_to_redis(self, audio_features):
        start_time = datetime.utcnow()
        print("{} exporting {} features to redis results queue...".format(start_time, len(audio_features)))
        for audio_feature in audio_features:
            self.redis_results_client.add(audio_feature.to_dict())
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
