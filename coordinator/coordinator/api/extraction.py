from logging import Logger

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode, ClientError
from commons.abstractions.flask_api import FlaskRestApi
from commons.models.extraction_request import ExtractionRequest
from commons.services.store_provider import FileStore
from commons.services.uuid_generation import generate_uuid
from extractor.engine.tasks import extract_feature
from extractor.task_api import run_task, retrieve_result, delete_result

NO_TASK_ID_IN_QUERY_PARAM = ClientError("Bad request: did not found task_id query param")


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


class ResultApi(FlaskRestApi):
    def _get(self, the_request: ApiRequest) -> ApiResponse:
        task_id = the_request.query_params.get("task_id")
        if task_id is not None:
            self.logger.info("Querying result of {}...".format(task_id))
            extraction_result = retrieve_result(task_id)
            self.logger.info("Returning result of {}: {}".format(task_id, extraction_result.status))
            return ApiResponse(HttpStatusCode.ok, extraction_result.to_serializable())
        else:
            raise NO_TASK_ID_IN_QUERY_PARAM

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        task_id = the_request.query_params.get("task_id")
        if task_id is not None:
            was_successful = delete_result(task_id)
            if was_successful:
                return ApiResponse(HttpStatusCode.ok, {"task_id": task_id})
            else:
                raise ClientError("Did not find result with given task id: {}".format(task_id),
                                  HttpStatusCode.bad_request)
        else:
            raise NO_TASK_ID_IN_QUERY_PARAM


class ExtractionApi(FlaskRestApi):
    def _post(self, the_request: ApiRequest) -> ApiResponse:
        execution_request = ExtractionRequest.from_serializable(the_request.payload)
        self.logger.info("Sending feature extraction task: {}...".format(execution_request))
        serialized_request = execution_request.to_serializable()
        task_id = generate_uuid(serialized_request)
        async_result = run_task(task=extract_feature,
                                task_id=task_id,
                                extraction_request=serialized_request)
        self.logger.info("Sent feature extraction task! ID: {}.".format(async_result.task_id))
        return ApiResponse(HttpStatusCode.accepted, {"task_id": async_result.task_id})
