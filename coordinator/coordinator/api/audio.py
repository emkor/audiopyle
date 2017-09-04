from commons.abstractions.api import AudiopyleRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.audio.file_meta import get_file_meta
from commons.utils.file_system import list_files, AUDIO_FILES_DIR, concatenate_paths


class AudioApi(AudiopyleRestApi):
    def get(self, request: ApiRequest):
        absolute_files_paths = [concatenate_paths(AUDIO_FILES_DIR, f) for f in list_files(AUDIO_FILES_DIR)]
        audio_files_metas = map(lambda p: get_file_meta(p), absolute_files_paths)
        return ApiResponse(HttpStatusCode.ok, list(audio_files_metas))
