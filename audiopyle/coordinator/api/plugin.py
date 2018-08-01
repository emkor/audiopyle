from logging import Logger

from audiopyle.commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from audiopyle.commons.abstractions.flask_api import FlaskRestApi
from audiopyle.commons.services.plugin_providing import VampyPluginProvider


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
