from commons.model.b2_config import B2Config
from commons.provider.b2_audio_provider import B2AudioProvider
from commons.service.os_env_accessor import OsEnvAccessor
from commons.utils.constant import AudiopyleConst
from coordinator.model.remote_file_meta import RemoteFileMeta


class B2Coordinator(object):
    def __init__(self,
                 audio_provider=None,
                 b2_config=B2Config(
                     AudiopyleConst.B2_ACCOUNT_ID,
                     AudiopyleConst.B2_APPLICATION_KEY,
                     AudiopyleConst.B2_RESOURCES_BUCKET),
                 local_cache_dir=OsEnvAccessor.get_env_variable(
                     AudiopyleConst.PROJECT_HOME_ENV)):

        self.audio_provider = audio_provider \
            or B2AudioProvider(b2_config, local_cache_dir)

    def get_remote_audio_files(self):
        file_infos = self.audio_provider.get_file_infos()
        audio_file_infos = self._filter_audio_files(file_infos)
        audio_file_infos.sort(key=lambda k: k[u'uploadTimestamp'])

        remote_audio_files = []
        for file in audio_file_infos:
            remote_audio_files.append(RemoteFileMeta(file[u'fileName'],
                                                     file[u'size'],
                                                     file[u'uploadTimestamp']))

        return remote_audio_files

    def _filter_audio_files(self, files):
        return [{u'fileName': file[u'fileName'],
                 u'size': file[u'size'],
                 u'uploadTimestamp': file[u'uploadTimestamp']}
                for file in files
                if u'audio' in file[u'contentType']]
