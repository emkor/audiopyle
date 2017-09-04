from commons.abstractions.api import AudiopyleRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from coordinator.utils import COORDINATOR_STATUS_RESPONSE


class CoordinatorApi(AudiopyleRestApi):
    def get(self, request: ApiRequest):
        return ApiResponse(status_code=HttpStatusCode.ok, payload={"status": COORDINATOR_STATUS_RESPONSE})
