from logging import Logger

from typing import List, Dict, Any

from audiopyle.lib.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from audiopyle.lib.abstractions.flask_api import FlaskRestApi
from audiopyle.lib.models.extraction_request import ExtractionRequest
from audiopyle.lib.models.plugin import VampyPlugin
from audiopyle.lib.repository.request import ResultRepository
from audiopyle.lib.services.audio_tag_providing import ACCEPTED_EXTENSIONS
from audiopyle.lib.services.metric_config_provider import MetricConfigProvider
from audiopyle.lib.services.plugin_config_provider import PluginConfigProvider
from audiopyle.lib.services.plugin_providing import VampyPluginProvider
from audiopyle.lib.services.store_provider import FileStore
from audiopyle.worker.engine.tasks import extract_feature
from audiopyle.worker.task_api import run_task


class AutomationApi(FlaskRestApi):
    def __init__(self, plugin_provider: VampyPluginProvider, plugin_config_provider: PluginConfigProvider,
                 metric_config_provider: MetricConfigProvider, audio_file_store: FileStore,
                 result_repo: ResultRepository, logger: Logger) -> None:
        super().__init__(logger)
        self.plugin_provider = plugin_provider
        self.plugin_config_provider = plugin_config_provider
        self.metric_config_provider = metric_config_provider
        self.audio_file_store = audio_file_store
        self.result_repo = result_repo

    def _post(self, the_request: ApiRequest) -> ApiResponse:
        audio_file_names = self.audio_file_store.list()
        plugins = self.plugin_provider.list_vampy_plugins()
        plugin_configs = self.plugin_config_provider.get_all() or {}

        if audio_file_names and plugins:
            extraction_requests = self._generate_extraction_requests(audio_file_names, plugins, plugin_configs)
            task_id_to_request = {r.uuid(): r.to_serializable() for r in extraction_requests}
            self.logger.debug("Sending {} extraction requests...".format(task_id_to_request))
            for task_id, request in task_id_to_request.items():
                if self.result_repo.exists_by_id(task_id):
                    self.logger.warning("Request {} #{} already exist in DB! Omitting...".format(request, task_id))
                else:
                    run_task(task=extract_feature, task_id=task_id, extraction_request=request)
                    self.logger.info("Sent feature extraction request {} with id {}...".format(request, task_id))
            return ApiResponse(HttpStatusCode.accepted, task_id_to_request)
        else:
            return ApiResponse(status_code=HttpStatusCode.no_content, payload=None)

    def _generate_extraction_requests(self, audio_file_names: List[str], plugins: List[VampyPlugin],
                                      plugin_configs: Dict[str, Dict[str, Any]]) -> List[ExtractionRequest]:
        extraction_requests = []
        for audio_file_name in audio_file_names:
            for plugin in plugins:
                plugin_metric_config = self.metric_config_provider.get_for_plugin(plugin_full_key=plugin.full_key)
                extraction_requests.append(
                    ExtractionRequest(audio_file_name=audio_file_name,
                                      plugin_full_key=plugin.full_key,
                                      plugin_config=plugin_configs.get(plugin.full_key, None),
                                      metric_config=plugin_metric_config or None))
        return extraction_requests
