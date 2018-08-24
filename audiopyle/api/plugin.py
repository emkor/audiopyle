from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode
from audiopyle.api.utils import build_request, log_api_call, build_response
from audiopyle.lib.services.plugin_providing import VampyPluginProvider


class PluginListApi(AbstractRestApi):
    def __init__(self, plugin_provider: VampyPluginProvider) -> None:
        self.plugin_provider = plugin_provider

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        api_response = ApiResponse(status_code=HttpStatusCode.ok, payload=self.plugin_provider.list_full_plugin_keys())
        log_api_call(api_request, api_response)
        return build_response(api_response)


class PluginDetailApi(AbstractRestApi):
    def __init__(self, plugin_provider: VampyPluginProvider) -> None:
        self.plugin_provider = plugin_provider

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            plugin_vendor = api_request.query_params["vendor"]
            plugin_name = api_request.query_params["name"]
            plugin_output = api_request.query_params["output"]
            vampy_plugins = self.plugin_provider.build_plugin_from_params(plugin_vendor, plugin_name, plugin_output)
            api_response = ApiResponse(status_code=HttpStatusCode.ok, payload=vampy_plugins.to_serializable())
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request, {
                "error": "Could not find vendor, name or output in request URL: {}".format(api_request.url)})
        log_api_call(api_request, api_response)
        return build_response(api_response)
