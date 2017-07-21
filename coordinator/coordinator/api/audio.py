from commons.abstractions.api import AudiopyleRestApi
from commons.audio.file_meta import get_file_meta
from commons.utils.file_system import list_files, AUDIO_FILES_DIR, concatenate_paths


class AudioApi(AudiopyleRestApi):
    def get(self, request_url, query_params):
        absolute_files_paths = [concatenate_paths(AUDIO_FILES_DIR, f) for f in list_files(AUDIO_FILES_DIR)]
        audio_files_metas = map(lambda p: get_file_meta(p), absolute_files_paths)
        return list(audio_files_metas)

    def post(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method

    def delete(self, request_url, query_params):
        raise self.not_implemented_api_method

    def put(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method
