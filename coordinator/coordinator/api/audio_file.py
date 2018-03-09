from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from commons.services.file_meta_providing import read_file_meta
from commons.utils.file_system import list_files, AUDIO_FILES_DIR, concatenate_paths


class AudioFileApi(FlaskRestApi):
    def _get(self, the_request: ApiRequest) -> ApiResponse:
        absolute_files_paths = [concatenate_paths(AUDIO_FILES_DIR, f) for f in list_files(AUDIO_FILES_DIR)]
        audio_files_metas = list(map(lambda p: read_file_meta(p).to_serializable(), absolute_files_paths))
        return ApiResponse(HttpStatusCode.ok, audio_files_metas)
