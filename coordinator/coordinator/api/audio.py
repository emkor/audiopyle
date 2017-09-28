from mutagen.easyid3 import EasyID3

from commons.abstractions.api import AudiopyleRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.audio.audio_tag import Id3Tag
from commons.audio.file_meta import get_file_meta
from commons.utils.file_system import list_files, AUDIO_FILES_DIR, concatenate_paths


class AudioApi(AudiopyleRestApi):
    def get(self, request: ApiRequest) -> ApiResponse:
        absolute_files_paths = [concatenate_paths(AUDIO_FILES_DIR, f) for f in list_files(AUDIO_FILES_DIR)]
        audio_files_metas = map(lambda p: get_file_meta(p), absolute_files_paths)
        return ApiResponse(HttpStatusCode.ok, list(audio_files_metas))


class AudioTagApi(AudiopyleRestApi):
    def get(self, request: ApiRequest):
        audio_file_name = request.query_params.get("file")
        self.logger.info("Reading ID3 tags of {}...".format(audio_file_name))
        full_audio_file_name = concatenate_paths("/home/mkorzeni/projects/audiopyle/resources/audio", audio_file_name)
        id3_tag = Id3Tag.from_easy_id3_object(EasyID3(full_audio_file_name))
        return ApiResponse(HttpStatusCode.ok, id3_tag.serialize())
