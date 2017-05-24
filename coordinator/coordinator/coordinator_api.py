from commons.api import AudiopyleRestApi
from commons.file_system import list_files
from commons.serializer import from_json, to_json
from coordinator.extraction_request import ExtractionRequest
from coordinator.vampy_plugin_provider import list_vampy_plugins

AUDIO_FILES_DIR = "/audio"
TMP_DIR = "/audio_tmp"
RESULTS_DIR = "/result"

COORDINATOR_STATUS_RESPONSE = {"api": "coordinator", "status": "ok"}


class CoordinatorApi(AudiopyleRestApi):
    def get(self, request_url, query_params):
        return COORDINATOR_STATUS_RESPONSE

    def post(self, request_url, query_params, request_payload):
        return self._read_request(request_payload)

    def delete(self, request_url, query_params):
        raise self.not_implemented_api_method

    def put(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method

    def _read_request(self, json):
        """
        :type json: dict
        :rtype: extracter.extraction_request.ExtractionRequest
        """
        return from_json(input_json=json, target_class=ExtractionRequest)


class PluginApi(AudiopyleRestApi):
    def get(self, request_url, query_params):
        return list_vampy_plugins()

    def post(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method

    def delete(self, request_url, query_params):
        raise self.not_implemented_api_method

    def put(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method


class AudioApi(AudiopyleRestApi):
    def get(self, request_url, query_params):
        return list_files(AUDIO_FILES_DIR)

    def post(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method

    def delete(self, request_url, query_params):
        raise self.not_implemented_api_method

    def put(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method


class ResultsApi(AudiopyleRestApi):
    def get(self, request_url, query_params):
        return list_files(RESULTS_DIR)

    def post(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method

    def delete(self, request_url, query_params):
        raise self.not_implemented_api_method

    def put(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method
