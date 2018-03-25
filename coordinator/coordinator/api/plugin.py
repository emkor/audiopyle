from logging import Logger

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from commons.services.plugin_config_provider import PluginConfigProvider
from commons.services.plugin_providing import VampyPluginProvider
from commons.utils.file_system import PLUGIN_CONFIG_IDENTIFIER


class PluginListApi(FlaskRestApi):
    def __init__(self, plugin_provider: VampyPluginProvider, logger: Logger) -> None:
        super().__init__(logger)
        self.plugin_provider = plugin_provider

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        return ApiResponse(status_code=HttpStatusCode.ok, payload=self.plugin_provider.list_full_plugin_keys())


class PluginDetailApi(FlaskRestApi):
    def __init__(self, plugin_provider: VampyPluginProvider, logger: Logger) -> None:
        super().__init__(logger)
        self.plugin_provider = plugin_provider

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        try:
            plugin_vendor = the_request.query_params["vendor"]
            plugin_name = the_request.query_params["name"]
            plugin_output = the_request.query_params["output"]
        except Exception:
            return ApiResponse(HttpStatusCode.bad_request, {
                "error": "Could not find vendor, name or output in request URL: {}".format(the_request.url)})
        vampy_plugins = self.plugin_provider.build_plugin_from_params(plugin_vendor, plugin_name, plugin_output)
        return ApiResponse(status_code=HttpStatusCode.ok, payload=vampy_plugins.to_serializable())


class PluginActiveConfigApi(FlaskRestApi):
    def __init__(self, plugin_config_provider: PluginConfigProvider, logger: Logger) -> None:
        super().__init__(logger)
        self.plugin_config_provider = plugin_config_provider

    def _get(self, the_request: ApiRequest):
        try:
            return ApiResponse(status_code=HttpStatusCode.ok, payload=self.plugin_config_provider.get_all())
        except Exception:
            return ApiResponse(HttpStatusCode.not_found,
                               {"error": "Could not find config file: {}".format(PLUGIN_CONFIG_IDENTIFIER)})
