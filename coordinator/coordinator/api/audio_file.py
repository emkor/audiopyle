from commons.abstractions.cherrypy_api import CherryPyRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.services.file_meta_providing import read_file_meta
from commons.utils.file_system import list_files, AUDIO_FILES_DIR, concatenate_paths, TMP_DIR, remove_file, \
    extract_extension


class AudioFileApi(CherryPyRestApi):
    def _get(self, request: ApiRequest) -> ApiResponse:
        absolute_files_paths = [concatenate_paths(AUDIO_FILES_DIR, f) for f in list_files(AUDIO_FILES_DIR)]
        audio_files_metas = list(map(lambda p: read_file_meta(p).to_serializable(), absolute_files_paths))
        return ApiResponse(HttpStatusCode.ok, audio_files_metas)


class TmpAudioApi(CherryPyRestApi):
    def _get(self, request: ApiRequest) -> ApiResponse:
        absolute_files_paths = [concatenate_paths(TMP_DIR, f) for f in list_files(TMP_DIR)]
        wav_absolute_file_paths = [f for f in absolute_files_paths if extract_extension(f) == "wav"]
        audio_files_metas = list(map(lambda p: read_file_meta(p).to_serializable(), wav_absolute_file_paths))
        return ApiResponse(HttpStatusCode.ok, audio_files_metas)

    def _delete(self, request: ApiRequest):
        absolute_files_paths = [concatenate_paths(TMP_DIR, f) for f in list_files(TMP_DIR)]
        self.logger.warning("Removing all {} tmp files...".format(len(absolute_files_paths)))
        for f in absolute_files_paths:
            remove_file(f)
        return ApiResponse(HttpStatusCode.ok, None)
