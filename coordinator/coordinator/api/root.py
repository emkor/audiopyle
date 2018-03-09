from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from coordinator.utils import COORDINATOR_STATUS_RESPONSE


class CoordinatorApi(FlaskRestApi):
    def _get(self, the_request: ApiRequest) -> ApiResponse:
        return ApiResponse(status_code=HttpStatusCode.ok, payload={"status": COORDINATOR_STATUS_RESPONSE})
