from commons.abstractions.cherrypy_api import CherryPyRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.services.plugin_providing import list_vampy_plugins


class PluginApi(CherryPyRestApi):
    def _get(self, the_request: ApiRequest) -> ApiResponse:
        vampy_plugins = list_vampy_plugins()
        return ApiResponse(status_code=HttpStatusCode.ok, payload=[p.to_serializable() for p in vampy_plugins])
