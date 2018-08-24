from flask import jsonify, make_response, Request

from audiopyle.lib.abstractions.api_model import ApiRequest, ApiResponse, HttpMethod
from audiopyle.lib.utils.conversion import seconds_between
from audiopyle.lib.utils.logger import get_logger

logger = get_logger()

COORDINATOR_STATUS_RESPONSE = "ok"


def build_response(the_response: ApiResponse) -> str:
    return make_response(jsonify(the_response.payload) if the_response.payload is not None else '',
                         the_response.status_code.value, the_response.headers or {})


def build_request(flask_request: Request, **kwargs) -> ApiRequest:
    return ApiRequest(url=flask_request.full_path, method=HttpMethod(flask_request.method), query_params=kwargs,
                      headers=flask_request.headers, payload=flask_request.json or {})


def log_api_call(api_request: ApiRequest, api_response: ApiResponse) -> None:
    serving_time = seconds_between(api_request.creation_time)
    logger.info("Served {} @ {} with {} ({} -> {}) in {}s.".format(api_request.method,
                                                                   api_request.url,
                                                                   api_response.status_code,
                                                                   api_request.size_humanized(),
                                                                   api_response.size_humanized(),
                                                                   serving_time))
