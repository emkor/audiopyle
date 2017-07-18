from commons.abstractions.api import AudiopyleRestApi
from commons.services.extraction import ExtractionRequest
from commons.utils.serialization import from_json
from coordinator.utils import COORDINATOR_STATUS_RESPONSE


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
