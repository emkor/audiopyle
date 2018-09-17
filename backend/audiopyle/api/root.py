from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode
from audiopyle.api.utils import build_request, log_api_call, build_response, COORDINATOR_STATUS_RESPONSE


class CoordinatorApi(AbstractRestApi):
    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        api_response = ApiResponse(status_code=HttpStatusCode.ok, payload={"status": COORDINATOR_STATUS_RESPONSE})
        log_api_call(api_request, api_response)
        return build_response(api_response)
