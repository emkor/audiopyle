from commons.abstractions.api import AudiopyleRestApi
from coordinator.utils import COORDINATOR_STATUS_RESPONSE


class CoordinatorApi(AudiopyleRestApi):
    def get(self, request_url, query_params):
        return COORDINATOR_STATUS_RESPONSE
