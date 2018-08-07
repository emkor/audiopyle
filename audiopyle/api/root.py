from audiopyle.lib.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from audiopyle.lib.abstractions.flask_api import FlaskRestApi
from audiopyle.api.utils import COORDINATOR_STATUS_RESPONSE


class CoordinatorApi(FlaskRestApi):
    def _get(self, the_request: ApiRequest) -> ApiResponse:
        return ApiResponse(status_code=HttpStatusCode.ok, payload={"status": COORDINATOR_STATUS_RESPONSE})
