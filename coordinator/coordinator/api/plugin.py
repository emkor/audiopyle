from commons.abstractions.api import AudiopyleRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.services.plugin_providing import list_vampy_plugins


class PluginApi(AudiopyleRestApi):
    def get(self, request: ApiRequest) -> ApiResponse:
        return ApiResponse(status_code=HttpStatusCode.ok, payload=list_vampy_plugins())
