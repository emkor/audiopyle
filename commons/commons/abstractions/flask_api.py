from logging import Logger

from flask import jsonify, request, make_response
from flask.views import MethodView

from commons.abstractions.api import AbstractRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpMethod


class FlaskRestApi(AbstractRestApi, MethodView):
    def __init__(self, logger: Logger = None) -> None:
        super().__init__(logger)

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        return super()._delete(the_request)

    def _put(self, the_request: ApiRequest) -> ApiResponse:
        return super()._put(the_request)

    def _post(self, the_request: ApiRequest) -> ApiResponse:
        return super()._post(the_request)

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        return super()._get(the_request)

    def get(self, **kwargs):
        the_request = ApiRequest(url=request.full_path, method=HttpMethod(request.method), query_params=kwargs,
                                 headers=request.headers, payload={})
        the_response = self._get(the_request)
        self._log_api_call(the_request, the_response)
        return make_response(jsonify(the_response.payload), the_response.status_code.value, the_response.headers or {})

    def post(self, **kwargs):
        the_request = ApiRequest(url=request.full_path, method=HttpMethod(request.method), query_params=kwargs,
                                 headers=request.headers, payload=request.json)
        the_response = self._post(the_request)
        self._log_api_call(the_request, the_response)
        return make_response(jsonify(the_response.payload), the_response.status_code.value, the_response.headers or {})

    def put(self, **kwargs):
        the_request = ApiRequest(url=request.full_path, method=HttpMethod(request.method), query_params=kwargs,
                                 headers=request.headers, payload=request.json)
        the_response = self._put(the_request)
        self._log_api_call(the_request, the_response)
        return make_response(jsonify(the_response.payload), the_response.status_code.value, the_response.headers or {})

    def delete(self, **kwargs):
        the_request = ApiRequest(url=request.full_path, method=HttpMethod(request.method), query_params=kwargs,
                                 headers=request.headers, payload={})
        the_response = self._delete(the_request)
        self._log_api_call(the_request, the_response)
        return make_response(jsonify(the_response.payload), the_response.status_code.value, the_response.headers or {})
