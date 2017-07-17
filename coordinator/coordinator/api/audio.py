from commons.abstractions.api import AudiopyleRestApi
from commons.utils.file_system import list_files, AUDIO_FILES_DIR


class AudioApi(AudiopyleRestApi):
    def get(self, request_url, query_params):
        return list_files(AUDIO_FILES_DIR)

    def post(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method

    def delete(self, request_url, query_params):
        raise self.not_implemented_api_method

    def put(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method
