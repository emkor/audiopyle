from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode
from audiopyle.api.utils import build_request, build_response, log_api_call
from audiopyle.lib.services.metric_config_provider import MetricConfigProvider
from audiopyle.lib.services.plugin_config_provider import PluginConfigProvider
from audiopyle.lib.utils.file_system import PLUGIN_CONFIG_FILE_NAME


class PluginConfigListApi(AbstractRestApi):
    def __init__(self, plugin_config_provider: PluginConfigProvider) -> None:
        self.plugin_config_provider = plugin_config_provider

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            api_response = ApiResponse(status_code=HttpStatusCode.ok, payload=self.plugin_config_provider.get_plugin_names())
        except Exception:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       {"message": "Could not find config file: {}".format(PLUGIN_CONFIG_FILE_NAME)})
        log_api_call(api_request, api_response)
        return build_response(api_response)


class PluginConfigApi(AbstractRestApi):
    def __init__(self, plugin_config_provider: PluginConfigProvider) -> None:
        self.plugin_config_provider = plugin_config_provider

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            vendor = api_request.query_params["vendor"]
            name = api_request.query_params["name"]
            output = api_request.query_params["output"]
            plugin_key = "{}:{}:{}".format(vendor, name, output)
            api_response = ApiResponse(status_code=HttpStatusCode.ok,
                                       payload=self.plugin_config_provider.get_for_plugin(plugin_key))
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       payload={"message": "Could not find plugin key parameter in URL: {}".format(
                                           api_request.url)})
        except Exception:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       {"message": "Could not find config file: {}".format(PLUGIN_CONFIG_FILE_NAME)})
        log_api_call(api_request, api_response)
        return build_response(api_response)


class MetricConfigListApi(AbstractRestApi):
    def __init__(self, metric_config_provider: MetricConfigProvider) -> None:
        self.metric_config_provider = metric_config_provider

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            api_response = ApiResponse(status_code=HttpStatusCode.ok,
                                       payload=self.metric_config_provider.get_metric_names())
        except Exception:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       {"message": "Could not find config file: {}".format(PLUGIN_CONFIG_FILE_NAME)})
        log_api_call(api_request, api_response)
        return build_response(api_response)


class MetricByNameApi(AbstractRestApi):
    def __init__(self, metric_config_provider: MetricConfigProvider) -> None:
        self.metric_config_provider = metric_config_provider

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            metric_name = api_request.query_params["name"]
            api_response = ApiResponse(status_code=HttpStatusCode.ok,
                                       payload=self.metric_config_provider.get_by_name(metric_name))
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       payload={"message": "Could not find metric name parameter in URL: {}".format(
                                           api_request.url)})
        except Exception:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       {"message": "Could not find config file: {}".format(PLUGIN_CONFIG_FILE_NAME)})
        log_api_call(api_request, api_response)
        return build_response(api_response)


class MetricsByPluginApi(AbstractRestApi):
    def __init__(self, metric_config_provider: MetricConfigProvider) -> None:
        self.metric_config_provider = metric_config_provider

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            vendor = api_request.query_params["vendor"]
            name = api_request.query_params["name"]
            output = api_request.query_params["output"]
            plugin_key = "{}:{}:{}".format(vendor, name, output)
            api_response = ApiResponse(status_code=HttpStatusCode.ok,
                                       payload=self.metric_config_provider.get_metric_names_for_plugin(plugin_key))
        except KeyError:
            message = "Could not find metric plugin parameters in URL: {}".format(api_request.url)
            api_response = ApiResponse(HttpStatusCode.bad_request, payload={"message": message})
        except Exception:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       {"message": "Could not find config file: {}".format(PLUGIN_CONFIG_FILE_NAME)})
        log_api_call(api_request, api_response)
        return build_response(api_response)
