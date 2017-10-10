from commons.abstractions.api import AudiopyleRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.services.uuid_generation import generate_uuid
from commons.utils.file_system import list_files, AUDIO_FILES_DIR, extract_extension
from commons.utils.logger import get_logger
from extractor.service import run_task
from extractor.tasks import extract_all_features

ACCEPTED_EXTENSIONS = ("mp3", "wav", "flac")

logger = get_logger()


class AutomationApi(AudiopyleRestApi):
    def get(self, request: ApiRequest) -> ApiResponse:
        all_file_names = list_files(AUDIO_FILES_DIR)
        audio_file_names = [f for f in all_file_names if extract_extension(f).lower() in ACCEPTED_EXTENSIONS]
        logger.info("Found audio file names: {}".format(audio_file_names))
        if audio_file_names:
            audio_file_name_to_task_id = {}
            for audio_file_name in audio_file_names:
                task_id = generate_uuid(audio_file_name)
                audio_file_name_to_task_id.update({audio_file_name: task_id})
                logger.info(
                    "Running extract_all_features task with id {} and file {}...".format(task_id, audio_file_name))
                run_task(task=extract_all_features, task_id=task_id, audio_file_name=audio_file_name)
            return ApiResponse(status_code=HttpStatusCode.accepted, payload=audio_file_name_to_task_id)
        else:
            return ApiResponse(status_code=HttpStatusCode.no_content,
                               payload="No audio files matching {} extensions found!".format(ACCEPTED_EXTENSIONS))
