from logging import Logger

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode, ClientError
from commons.abstractions.flask_api import FlaskRestApi
from commons.services.store_provider import FileStore


class ResultListApi(FlaskRestApi):
    def __init__(self, file_store: FileStore, logger: Logger):
        super().__init__(logger)
        self.file_store = file_store
        self.logger = logger

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        return ApiResponse(HttpStatusCode.ok, self.file_store.list())


class ResultDetailsApi(FlaskRestApi):
    def __init__(self, file_store: FileStore, logger: Logger):
        super().__init__(logger)
        self.file_store = file_store
        self.logger = logger

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        task_id = the_request.query_params.get("task_id")
        if self.file_store.exists(task_id):
            return ApiResponse(HttpStatusCode.ok, self.file_store.read(task_id))
        else:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        task_id = the_request.query_params.get("task_id")
        if self.file_store.exists(task_id):
            return ApiResponse(HttpStatusCode.ok, self.file_store.remove(task_id))
        else:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})
