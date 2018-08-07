from logging import Logger

from audiopyle.lib.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from audiopyle.lib.abstractions.flask_api import FlaskRestApi
from audiopyle.lib.services.store_provider import FileStore


class AudioFileListApi(FlaskRestApi):
    def __init__(self, file_store: FileStore, logger: Logger) -> None:
        super().__init__(logger)
        self.file_store = file_store

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        return ApiResponse(HttpStatusCode.ok, self.file_store.list())


class AudioFileDetailApi(FlaskRestApi):
    def __init__(self, file_store: FileStore, logger: Logger) -> None:
        super().__init__(logger)
        self.file_store = file_store

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        file_name = the_request.query_params["file_name"]
        if self.file_store.exists(file_name):
            return ApiResponse(HttpStatusCode.ok, self.file_store.meta(file_name).to_serializable())
        else:
            return ApiResponse(HttpStatusCode.not_found,
                               {"error": "Can't find file with name: {}".format(file_name)})
