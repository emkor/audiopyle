from coordinator.model.remote_audio_file import RemoteAudioFile
from commons.provider.b2_audio_provider import B2AudioProvider


class B2Coordinator(object):
    def __init__(self, b2_config, local_cache_dir):
        self.audio_provider = B2AudioProvider(b2_config, local_cache_dir)

    def get_remote_audio_files(self):
        file_infos = self.audio_provider.get_file_infos()
        audio_file_infos = [{u'fileName': i[u'fileName'],
                             u'size': i[u'size'],
                             u'uploadTimestamp': i[u'uploadTimestamp']}
                            for i in file_infos
                            if u'audio' in i[u'contentType']]

        audio_file_infos.sort(key=lambda k: k[u'uploadTimestamp'])

        self.remote_audio_files = []
        for i in audio_file_infos:
            self.remote_audio_files.append(RemoteAudioFile(i[u'fileName'],
                                                           i[u'size'],
                                                           i[u'uploadTimestamp']))
