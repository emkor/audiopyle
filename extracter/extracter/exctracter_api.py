from commons.api import AudiopyleApi
from commons.file_system import list_files
from extracter.vampy_plugin_provider import list_vampy_plugins

AUDIO_FILES_DIR = "/audio"
TMP_DIR = "/audio_tmp"


class ExtracterApi(AudiopyleApi):
    def get(self, request_url, query_params):
        return {"api": "extracter", "status": "ok"}

    def post(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method

    def delete(self, request_url, query_params):
        raise self.not_implemented_api_method

    def put(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method


class PluginApi(AudiopyleApi):
    def get(self, request_url, query_params):
        return list_vampy_plugins()

    def post(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method

    def delete(self, request_url, query_params):
        raise self.not_implemented_api_method

    def put(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method


class AudioApi(AudiopyleApi):
    def get(self, request_url, query_params):
        return list_files(AUDIO_FILES_DIR)

    def post(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method

    def delete(self, request_url, query_params):
        raise self.not_implemented_api_method

    def put(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method
