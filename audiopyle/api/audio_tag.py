from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode
from audiopyle.api.utils import build_request, build_response, log_api_call
from audiopyle.lib.services.audio_tag_providing import read_audio_tag, ACCEPTED_EXTENSIONS
from audiopyle.lib.utils.file_system import AUDIO_FILES_DIR, concatenate_paths, extract_extension


class AudioTagApi(AbstractRestApi):
    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        audio_file_name = api_request.query_params["file_name"]
        if extract_extension(audio_file_name) in ACCEPTED_EXTENSIONS:
            audio_file_absolute_path = concatenate_paths(AUDIO_FILES_DIR, audio_file_name)
            id3_tag = read_audio_tag(audio_file_absolute_path)
            if id3_tag:
                api_response = ApiResponse(HttpStatusCode.ok, id3_tag.to_serializable())
            else:
                api_response = ApiResponse(HttpStatusCode.not_found,
                                           {"error": "Could not read tag from: {}".format(audio_file_name)})
        else:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       "Can not read tags from non-mp3 file: {}".format(audio_file_name))
        log_api_call(api_request, api_response)
        return build_response(api_response)
