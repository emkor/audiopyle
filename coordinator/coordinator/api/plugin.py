from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from commons.services.plugin_providing import list_plugin_keys, build_plugin_from_key


class PluginListApi(FlaskRestApi):
    def _get(self, the_request: ApiRequest) -> ApiResponse:
        return ApiResponse(status_code=HttpStatusCode.ok, payload=list_plugin_keys())


class PluginDetailApi(FlaskRestApi):
    def _get(self, the_request: ApiRequest) -> ApiResponse:
        plugin_vendor = the_request.query_params.get("vendor")
        plugin_name = the_request.query_params.get("name")
        vampy_plugin = build_plugin_from_key("{}:{}".format(plugin_vendor, plugin_name))
        return ApiResponse(status_code=HttpStatusCode.ok, payload=vampy_plugin.to_serializable())
