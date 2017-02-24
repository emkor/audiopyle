from commons.api import AudiopyleApi
from commons.file_system import list_files
from extracter.vampy_plugin_provider import list_vampy_plugins

AUDIO_FILES_DIR = "/audio"
TMP_DIR = "/audio_tmp"


class ExtracterApi(AudiopyleApi):
    def get(self, *args, **query_params):
        return {"api": "extracter", "status": "ok"}

    def post(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD

    def delete(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD

    def put(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD


class PluginApi(AudiopyleApi):
    def get(self, *args, **query_params):
        return list_vampy_plugins()

    def post(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD

    def delete(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD

    def put(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD


class AudioApi(AudiopyleApi):
    def get(self, *args, **query_params):
        return list_files(AUDIO_FILES_DIR)

    def post(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD

    def delete(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD

    def put(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD
