from logging import Logger

from typing import List, Dict, Any

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from commons.models.extraction_request import ExtractionRequest
from commons.models.plugin import VampyPlugin
from commons.repository.result import ResultRepository
from commons.services.audio_tag_providing import ACCEPTED_EXTENSIONS
from commons.services.plugin_config_provider import PluginConfigProvider
from commons.services.plugin_providing import VampyPluginProvider
from commons.services.store_provider import FileStore
from extractor.engine.tasks import extract_feature
from extractor.task_api import run_task


class AutomationApi(FlaskRestApi):
    def __init__(self, plugin_provider: VampyPluginProvider, plugin_config_provider: PluginConfigProvider,
                 audio_file_store: FileStore,
                 result_repo: ResultRepository, logger: Logger) -> None:
        super().__init__(logger)
        self.plugin_provider = plugin_provider
        self.plugin_config_provider = plugin_config_provider
        self.audio_file_store = audio_file_store
        self.result_repo = result_repo

    def _post(self, the_request: ApiRequest) -> ApiResponse:
        audio_file_identifiers = self.audio_file_store.list()
        plugins = self.plugin_provider.list_vampy_plugins()
        plugin_configs = self.plugin_config_provider.get_all()

        if audio_file_identifiers and plugins:
            extraction_requests = self._generate_extraction_requests(audio_file_identifiers, plugins, plugin_configs)
            task_id_to_request = {r.uuid(): r.to_serializable() for r in extraction_requests}
            self.logger.debug("Sending {} extraction requests...".format(task_id_to_request))
            for task_id, the_request in task_id_to_request.items():
                if self.result_repo.exists_by_id(task_id):
                    self.logger.warning("Request {} #{} already exist in DB! Omitting...".format(the_request, task_id))
                else:
                    run_task(task=extract_feature, task_id=task_id, extraction_request=the_request)
                    self.logger.info("Sent feature extraction request {} with id {}...".format(the_request, task_id))
            return ApiResponse(HttpStatusCode.accepted, task_id_to_request)
        elif not audio_file_identifiers:
            return ApiResponse(status_code=HttpStatusCode.no_content,
                               payload="No audio files matching {} extensions found!".format(ACCEPTED_EXTENSIONS))
        elif not plugins:
            return ApiResponse(status_code=HttpStatusCode.no_content, payload="No whitelisted plugins found!")

    def _generate_extraction_requests(self, audio_file_identifiers: List[str], plugins: List[VampyPlugin],
                                      plugin_configs: Dict[str, Dict[str, Any]]) -> List[ExtractionRequest]:
        extraction_requests = []
        for audio_file_identifier in audio_file_identifiers:
            for plugin in plugins:
                extraction_requests.append(
                    ExtractionRequest(audio_file_identifier=audio_file_identifier,
                                      plugin_full_key=plugin.full_key,
                                      plugin_config=plugin_configs.get(plugin.full_key, {})))
        return extraction_requests
