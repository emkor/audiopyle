from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode
from audiopyle.api.utils import build_request, build_response, log_api_call
from audiopyle.lib.services.metric_config_provider import MetricConfigProvider
from audiopyle.lib.services.plugin_config_provider import PluginConfigProvider
from audiopyle.lib.utils.file_system import PLUGIN_CONFIG_FILE_NAME


class PluginActiveConfigApi(AbstractRestApi):
    def __init__(self, plugin_config_provider: PluginConfigProvider) -> None:
        self.plugin_config_provider = plugin_config_provider

    def get(self, **kwargs) -> str:
        """Returns available plugin configuration per plugin
        ---
        responses:
            200:
                description: Content of plugin config JSON file
                schema:
                    type: object
                    additionalProperties:
                        type: object
                        properties:
                            block_size:
                                type: integer
                                nullable: true
                            step_size:
                                type: integer
                                nullable: true
                        additionalProperties: true
                examples:
                    application/json: |-
                        {
                            "vamp-example-plugins:amplitudefollower:amplitude": {
                                "block_size":4096,
                                "step_size":4096
                            }
                        }
            404:
                description: There was no plugin config file found
        """
        api_request = build_request(request, **kwargs)
        try:
            api_response = ApiResponse(status_code=HttpStatusCode.ok, payload=self.plugin_config_provider.get_all())
        except Exception:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       {"error": "Could not find config file: {}".format(PLUGIN_CONFIG_FILE_NAME)})
        log_api_call(api_request, api_response)
        return build_response(api_response)


class MetricActiveConfigApi(AbstractRestApi):
    def __init__(self, metric_config_provider: MetricConfigProvider) -> None:
        self.metric_config_provider = metric_config_provider

    def get(self, **kwargs) -> str:
        """Returns available plugin configuration per plugin
        ---
        responses:
            200:
                description: Content of metric config JSON file
                schema:
                    type: object
                    additionalProperties:
                        type: object
                        properties:
                            plugin:
                                type: string
                            transformation:
                                type: object
                                properties:
                                    name:
                                        type: string
                                    kwargs:
                                        type: object
                                        additionalProperties: true
                examples:
                    application/json: |-
                        {
                            "bbc_energy_average_rms": {
                                "plugin":"bbc-vamp-plugins:bbc-energy:average",
                                "transformation": {
                                    "name":"none"
                                }
                            }
                        }
            404:
                description: There was no metric config file found
        """
        api_request = build_request(request, **kwargs)
        try:
            api_response = ApiResponse(status_code=HttpStatusCode.ok, payload=self.metric_config_provider.get_all())
        except Exception:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       {"error": "Could not find config file: {}".format(PLUGIN_CONFIG_FILE_NAME)})
        log_api_call(api_request, api_response)
        return build_response(api_response)
