from logging import Logger

from audiopyle.lib.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from audiopyle.lib.abstractions.flask_api import FlaskRestApi
from audiopyle.lib.services.metric_config_provider import MetricConfigProvider
from audiopyle.lib.services.plugin_config_provider import PluginConfigProvider
from audiopyle.lib.utils.file_system import PLUGIN_CONFIG_FILE_NAME


class PluginActiveConfigApi(FlaskRestApi):
    def __init__(self, plugin_config_provider: PluginConfigProvider, logger: Logger) -> None:
        super().__init__(logger)
        self.plugin_config_provider = plugin_config_provider

    def _get(self, the_request: ApiRequest):
        try:
            return ApiResponse(status_code=HttpStatusCode.ok, payload=self.plugin_config_provider.get_all())
        except Exception:
            return ApiResponse(HttpStatusCode.not_found,
                               {"error": "Could not find config file: {}".format(PLUGIN_CONFIG_FILE_NAME)})


class MetricActiveConfigApi(FlaskRestApi):
    def __init__(self, metric_config_provider: MetricConfigProvider, logger: Logger) -> None:
        super().__init__(logger)
        self.metric_config_provider = metric_config_provider

    def _get(self, the_request: ApiRequest):
        try:
            return ApiResponse(status_code=HttpStatusCode.ok, payload=self.metric_config_provider.get_all())
        except Exception:
            return ApiResponse(HttpStatusCode.not_found,
                               {"error": "Could not find config file: {}".format(PLUGIN_CONFIG_FILE_NAME)})
