from commons.abstractions.api import AudiopyleRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.services.audio_tag_providing import read_id3_tag
from commons.services.file_meta_providing import read_mp3_file_meta
from commons.utils.file_system import list_files, AUDIO_FILES_DIR, concatenate_paths, extract_extension


class AudioApi(AudiopyleRestApi):
    def get(self, request: ApiRequest) -> ApiResponse:
        absolute_files_paths = [concatenate_paths(AUDIO_FILES_DIR, f) for f in list_files(AUDIO_FILES_DIR)]
        mp3_absolute_file_paths = [f for f in absolute_files_paths if extract_extension(f) == "mp3"]
        audio_files_metas = list(map(lambda p: read_mp3_file_meta(p).to_serializable(), mp3_absolute_file_paths))
        return ApiResponse(HttpStatusCode.ok, audio_files_metas)


class AudioTagApi(AudiopyleRestApi):
    def get(self, request: ApiRequest):
        audio_file_name = request.query_params.get("file")
        self.logger.info("Reading ID3 tags of {}...".format(audio_file_name))
        if extract_extension(audio_file_name) == "mp3":
            audio_file_absolute_path = concatenate_paths(AUDIO_FILES_DIR, audio_file_name)
            id3_tag = read_id3_tag(audio_file_absolute_path)
            return ApiResponse(HttpStatusCode.ok, id3_tag.to_serializable())
        else:
            return ApiResponse(HttpStatusCode.bad_request,
                               "Can not read tags from non-mp3 file: {}".format(audio_file_name))
