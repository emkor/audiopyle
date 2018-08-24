from flask import request
from flask.views import MethodView

from audiopyle.api.utils import build_response
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode, HttpMethod


def prepare_method_not_supported_response(method: HttpMethod) -> str:
    payload = {"error": "URL {} does not support {} method".format(request.full_path, method.value)}
    return build_response(ApiResponse(HttpStatusCode.method_not_allowed, payload))


class AbstractRestApi(MethodView):
    def get(self, **kwargs) -> str:
        return prepare_method_not_supported_response(HttpMethod.GET)

    def post(self, **kwargs) -> str:
        return prepare_method_not_supported_response(HttpMethod.POST)

    def put(self, **kwargs) -> str:
        return prepare_method_not_supported_response(HttpMethod.PUT)

    def delete(self, **kwargs) -> str:
        return prepare_method_not_supported_response(HttpMethod.DELETE)
