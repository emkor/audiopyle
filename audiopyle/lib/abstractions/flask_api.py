from logging import Logger

from flask import jsonify, request, make_response
from flask.views import MethodView

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiRequest, ApiResponse, HttpMethod, _ApiError


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
        try:
            the_response = self._get(the_request)
            self._log_api_call(the_request, the_response)
            return make_response(self._build_json(the_response), the_response.status_code.value,
                                 the_response.headers or {})
        except _ApiError as e:
            self.logger.warning(e)
            return make_response(jsonify({"error": e.message}), e.status_code.value, {})

    def post(self, **kwargs):
        the_request = ApiRequest(url=request.full_path, method=HttpMethod(request.method), query_params=kwargs,
                                 headers=request.headers, payload=request.json)
        try:
            the_response = self._post(the_request)
            self._log_api_call(the_request, the_response)
            return make_response(self._build_json(the_response), the_response.status_code.value,
                                 the_response.headers or {})
        except _ApiError as e:
            self.logger.warning(e)
            return make_response(jsonify({"error": e.message}), e.status_code.value, {})

    def put(self, **kwargs):
        the_request = ApiRequest(url=request.full_path, method=HttpMethod(request.method), query_params=kwargs,
                                 headers=request.headers, payload=request.json)
        try:
            the_response = self._put(the_request)
            self._log_api_call(the_request, the_response)
            return make_response(self._build_json(the_response), the_response.status_code.value,
                                 the_response.headers or {})
        except _ApiError as e:
            self.logger.warning(e)
            return make_response(jsonify({"error": e.message}), e.status_code.value, {})

    def delete(self, **kwargs):
        the_request = ApiRequest(url=request.full_path, method=HttpMethod(request.method), query_params=kwargs,
                                 headers=request.headers, payload={})
        try:
            the_response = self._delete(the_request)
            self._log_api_call(the_request, the_response)
            return make_response(self._build_json(the_response), the_response.status_code.value,
                                 the_response.headers or {})
        except _ApiError as e:
            self.logger.warning(e)
            return make_response(jsonify({"error": e.message}), e.status_code.value, {})

    def _build_json(self, the_response: ApiResponse) -> str:
        return jsonify(the_response.payload) if the_response.payload is not None else ''
