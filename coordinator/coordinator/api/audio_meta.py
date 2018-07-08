from mutagen.easyid3 import EasyID3

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from commons.services.audio_tag_providing import read_audio_tag, ACCEPTED_EXTENSIONS
from commons.services.file_meta_providing import read_mp3_file_meta
from commons.utils.file_system import AUDIO_FILES_DIR, concatenate_paths, extract_extension, file_exists


class AudioMetaApi(FlaskRestApi):
    def _get(self, the_request: ApiRequest) -> ApiResponse:
        audio_file_absolute_path = concatenate_paths(AUDIO_FILES_DIR, the_request.query_params.get("file_name"))
        if file_exists(audio_file_absolute_path):
            audio_files_meta = read_mp3_file_meta(audio_file_absolute_path)
            return ApiResponse(HttpStatusCode.ok, audio_files_meta.to_serializable())
        else:
            return ApiResponse(HttpStatusCode.not_found,
                               "Given file: {} does not exist".format(audio_file_absolute_path))


class AudioTagApi(FlaskRestApi):
    def _get(self, the_request: ApiRequest):
        audio_file_name = the_request.query_params.get("file_name")
        self.logger.info("Reading ID3 tags of {}...".format(audio_file_name))
        if extract_extension(audio_file_name) in ACCEPTED_EXTENSIONS:
            audio_file_absolute_path = concatenate_paths(AUDIO_FILES_DIR, audio_file_name)
            id3_tag = read_audio_tag(audio_file_absolute_path, EasyID3)
            return ApiResponse(HttpStatusCode.ok, id3_tag.to_serializable())
        else:
            return ApiResponse(HttpStatusCode.bad_request,
                               "Can not read tags from non-mp3 file: {}".format(audio_file_name))
