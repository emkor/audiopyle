from typing import List, Dict, Any

from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode
from audiopyle.api.utils import build_request, build_response, log_api_call
from audiopyle.lib.models.extraction_request import ExtractionRequest
from audiopyle.lib.models.plugin import VampyPlugin
from audiopyle.lib.repository.request import RequestRepository
from audiopyle.lib.services.metric_config_provider import MetricConfigProvider
from audiopyle.lib.services.plugin_config_provider import PluginConfigProvider
from audiopyle.lib.services.plugin_providing import VampyPluginProvider
from audiopyle.lib.services.store_provider import FileStore
from audiopyle.worker.engine.tasks import extract_feature
from audiopyle.worker.task_api import run_task


class AutomationApi(AbstractRestApi):
    def __init__(self, plugin_provider: VampyPluginProvider, plugin_config_provider: PluginConfigProvider,
                 metric_config_provider: MetricConfigProvider, audio_file_store: FileStore,
                 result_repo: RequestRepository) -> None:
        self.plugin_provider = plugin_provider
        self.plugin_config_provider = plugin_config_provider
        self.metric_config_provider = metric_config_provider
        self.audio_file_store = audio_file_store
        self.result_repo = result_repo

    def post(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        audio_file_names = self.audio_file_store.list()
        plugins = self.plugin_provider.list_vampy_plugins()
        plugin_configs = self.plugin_config_provider.get_all() or {}

        if audio_file_names and plugins:
            extraction_requests = self._generate_extraction_requests(audio_file_names, plugins, plugin_configs)
            for task_request in extraction_requests:
                if not self.result_repo.exists_by_id(task_request.task_id):
                    run_task(task=extract_feature, task_id=task_request.task_id,
                             extraction_request=task_request.to_serializable())
            api_response = ApiResponse(HttpStatusCode.accepted, [er.to_serializable() for er in extraction_requests])
        else:
            api_response = ApiResponse(status_code=HttpStatusCode.precondition_failed, payload=None)
        log_api_call(api_request, api_response)
        return build_response(api_response)

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
