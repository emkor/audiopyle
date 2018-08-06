from audiopyle.commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from audiopyle.commons.abstractions.flask_api import FlaskRestApi
from audiopyle.commons.services.audio_tag_providing import read_audio_tag, ACCEPTED_EXTENSIONS
from audiopyle.commons.utils.file_system import AUDIO_FILES_DIR, concatenate_paths, extract_extension


class AudioTagApi(FlaskRestApi):
    def _get(self, the_request: ApiRequest) -> ApiResponse:
        audio_file_name = the_request.query_params["file_name"]
        self.logger.info("Reading audio tags of {}...".format(audio_file_name))
        if extract_extension(audio_file_name) in ACCEPTED_EXTENSIONS:
            audio_file_absolute_path = concatenate_paths(AUDIO_FILES_DIR, audio_file_name)
            id3_tag = read_audio_tag(audio_file_absolute_path)
            if id3_tag:
                return ApiResponse(HttpStatusCode.ok, id3_tag.to_serializable())
            else:
                return ApiResponse(HttpStatusCode.not_found,
                                   {"error": "Could not read tag from: {}".format(audio_file_name)})
        else:
            return ApiResponse(HttpStatusCode.bad_request,
                               "Can not read tags from non-mp3 file: {}".format(audio_file_name))
