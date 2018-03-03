from commons.abstractions.api import CherryPyRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from coordinator.utils import COORDINATOR_STATUS_RESPONSE


class CoordinatorApi(CherryPyRestApi):
    def _get(self, request: ApiRequest) -> ApiResponse:
        return ApiResponse(status_code=HttpStatusCode.ok, payload={"status": COORDINATOR_STATUS_RESPONSE})
