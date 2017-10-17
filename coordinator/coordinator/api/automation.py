from commons.abstractions.api import AudiopyleRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.services.automation import ACCEPTED_EXTENSIONS, generate_extraction_requests, whitelisted_plugins, \
    allowed_audio_files
from extractor.service import run_task
from extractor.tasks import extract_feature


class AutomationApi(AudiopyleRestApi):
    def get(self, request: ApiRequest) -> ApiResponse:
        audio_file_names = allowed_audio_files()
        plugins = whitelisted_plugins()

        if audio_file_names and plugins:
            extraction_requests = generate_extraction_requests(audio_file_names, plugins)
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
