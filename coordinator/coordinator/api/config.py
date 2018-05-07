from logging import Logger

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from commons.services.metric_config_provider import MetricConfigProvider
from commons.services.plugin_config_provider import PluginConfigProvider
from commons.utils.file_system import PLUGIN_CONFIG_IDENTIFIER


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


class MetricActiveConfigApi(FlaskRestApi):
    def __init__(self, metric_config_provider: MetricConfigProvider, logger: Logger) -> None:
        super().__init__(logger)
        self.metric_config_provider = metric_config_provider

    def _get(self, the_request: ApiRequest):
        try:
            return ApiResponse(status_code=HttpStatusCode.ok, payload=self.metric_config_provider.get_all())
        except Exception:
            return ApiResponse(HttpStatusCode.not_found,
                               {"error": "Could not find config file: {}".format(PLUGIN_CONFIG_IDENTIFIER)})
