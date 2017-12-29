from typing import Text, List

from commons.abstractions.api import AudiopyleRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.models.plugin import VampyPlugin
from commons.services.feature_extraction import ExtractionRequest
from commons.services.plugin_providing import list_vampy_plugins
from commons.utils.env_var import get_environment_variable
from commons.utils.file_system import list_files, AUDIO_FILES_DIR, extract_extension
from extractor.service import run_task
from extractor.tasks import extract_feature

ACCEPTED_EXTENSIONS = ("mp3", "wav", "flac")


class AutomationApi(AudiopyleRestApi):
    def get(self, request: ApiRequest) -> ApiResponse:
        audio_file_names = self._allowed_audio_files()
        plugins = self._whitelisted_plugins()

        if audio_file_names and plugins:
            extraction_requests = self._generate_extraction_requests(audio_file_names, plugins)
            task_id_to_request = {r.uuid(): r.serialize() for r in extraction_requests}
            self.logger.info("Sending {} extraction requests...".format(task_id_to_request))
            for task_id, request in task_id_to_request.items():
                run_task(task=extract_feature, task_id=task_id, extraction_request=request)
                self.logger.info("Sent feature extraction request {} with id {}...".format(request, task_id))
            return ApiResponse(HttpStatusCode.accepted, task_id_to_request)
        elif not audio_file_names:
            return ApiResponse(status_code=HttpStatusCode.no_content,
                               payload="No audio files matching {} extensions found!".format(ACCEPTED_EXTENSIONS))
        elif not plugins:
            return ApiResponse(status_code=HttpStatusCode.no_content, payload="No whitelisted plugins found!")

    def _generate_extraction_requests(self, audio_file_names: List[Text],
                                      plugins: List[VampyPlugin]) -> List[ExtractionRequest]:
        extraction_requests = []
        for audio_file_name in audio_file_names:
            for plugin in plugins:
                for plugin_output in plugin.outputs:
                    extraction_requests.append(
                        ExtractionRequest(audio_file_name=audio_file_name, plugin_key=plugin.key,
                                          plugin_output=plugin_output))
        return extraction_requests

    def _allowed_audio_files(self):
        all_file_names = list_files(AUDIO_FILES_DIR)
        audio_file_names = [f for f in all_file_names if extract_extension(f).lower() in ACCEPTED_EXTENSIONS]
        if len(audio_file_names) != len(all_file_names):
            self.logger.warning("Omitted {} audio files because invalid extensions (accepted ones: {})".format(
                len(all_file_names) - len(audio_file_names), ACCEPTED_EXTENSIONS))
        self.logger.info("Found audio file names: {}".format(audio_file_names))
        return audio_file_names

    def _whitelisted_plugins(self) -> List[VampyPlugin]:
        blacklisted_plugins = get_environment_variable(variable_name="BLACKLISTED_PLUGINS", expected_type=str,
                                                       default="").split(",")
        if blacklisted_plugins:
            self.logger.warning(
                "Omitting blacklisted plugins ({}): {}...".format(len(blacklisted_plugins), blacklisted_plugins))
        plugins = list_vampy_plugins(blacklisted_plugins)
        return plugins
