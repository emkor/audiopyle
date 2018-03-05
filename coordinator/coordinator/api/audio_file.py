from logging import Logger

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from commons.services.store_provider import FileStore


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
        file_identifier = the_request.query_params.get("identifier")
        if self.file_store.exists(file_identifier):
            return ApiResponse(HttpStatusCode.ok, self.file_store.meta(file_identifier))
        else:
            return ApiResponse(HttpStatusCode.not_found,
                               {"error": "Can't find file with identifier: {}".format(file_identifier)})
