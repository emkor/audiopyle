from logging import Logger

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from commons.services.plugin_providing import VampyPluginProvider


class PluginListApi(FlaskRestApi):
    def __init__(self, plugin_provider: VampyPluginProvider, logger: Logger) -> None:
        super().__init__(logger)
        self.plugin_provider = plugin_provider

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        vampy_plugins = self.plugin_provider.list_vampy_plugins()
        return ApiResponse(status_code=HttpStatusCode.ok, payload=[vp.to_serializable() for vp in vampy_plugins])


class PluginDetailApi(FlaskRestApi):
    def __init__(self, plugin_provider: VampyPluginProvider, logger: Logger) -> None:
        super().__init__(logger)
        self.plugin_provider = plugin_provider

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        plugin_vendor = the_request.query_params.get("vendor")
        plugin_name = the_request.query_params.get("name")
        plugin_output = the_request.query_params.get("output")
        vampy_plugins = self.plugin_provider.build_plugin_from_params(plugin_vendor, plugin_name, plugin_output)
        return ApiResponse(status_code=HttpStatusCode.ok, payload=vampy_plugins.to_serializable())
