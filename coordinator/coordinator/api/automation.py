from logging import Logger

from typing import Text, List

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from commons.models.extraction_request import ExtractionRequest
from commons.models.plugin import VampyPlugin
from commons.services.audio_tag_providing import ACCEPTED_EXTENSIONS
from commons.services.plugin_providing import list_vampy_plugins
from commons.services.store_provider import FileStore
from commons.utils.env_var import read_env_var
from extractor.engine.tasks import extract_feature
from extractor.task_api import run_task


class AutomationApi(FlaskRestApi):
    def __init__(self, audio_file_store: FileStore, logger: Logger):
        super().__init__(logger)
        self.audio_file_store = audio_file_store

    def _post(self, the_request: ApiRequest) -> ApiResponse:
        audio_file_identifiers = self.audio_file_store.list()
        plugins = self._whitelisted_plugins()

        if audio_file_identifiers and plugins:
            extraction_requests = self._generate_extraction_requests(audio_file_identifiers, plugins)
            task_id_to_request = {r.uuid(): r.to_serializable() for r in extraction_requests}
            self.logger.info("Sending {} extraction requests...".format(task_id_to_request))
            for task_id, the_request in task_id_to_request.items():
                run_task(task=extract_feature, task_id=task_id, extraction_request=the_request)
                self.logger.info("Sent feature extraction request {} with id {}...".format(the_request, task_id))
            return ApiResponse(HttpStatusCode.accepted, task_id_to_request)
        elif not audio_file_identifiers:
            return ApiResponse(status_code=HttpStatusCode.no_content,
                               payload="No audio files matching {} extensions found!".format(ACCEPTED_EXTENSIONS))
        elif not plugins:
            return ApiResponse(status_code=HttpStatusCode.no_content, payload="No whitelisted plugins found!")

    def _generate_extraction_requests(self, audio_file_identifier: List[Text],
                                      plugins: List[VampyPlugin]) -> List[ExtractionRequest]:
        extraction_requests = []
        for audio_file_identifier in audio_file_identifier:
            for plugin in plugins:
                for plugin_output in plugin.outputs:
                    extraction_requests.append(
                        ExtractionRequest(audio_file_identifier=audio_file_identifier,
                                          plugin_key=plugin.key,
                                          plugin_output=plugin_output))
        return extraction_requests

    def _whitelisted_plugins(self) -> List[VampyPlugin]:
        blacklisted_plugins = read_env_var(var_name="BLACKLISTED_PLUGINS", expected_type=str,
                                           default="").split(",")
        if blacklisted_plugins:
            self.logger.warning(
                "Omitting blacklisted plugins ({}): {}...".format(len(blacklisted_plugins), blacklisted_plugins))
        plugins = list_vampy_plugins(blacklisted_plugins)
        return plugins
