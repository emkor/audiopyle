from logging import Logger

from audiopyle.lib.repository.request import RequestRepository
from audiopyle.lib.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode, ClientError
from audiopyle.lib.abstractions.flask_api import FlaskRestApi
from audiopyle.lib.models.extraction_request import ExtractionRequest
from audiopyle.worker.engine.tasks import extract_feature
from audiopyle.worker.result_model import TaskStatus
from audiopyle.worker.task_api import run_task, retrieve_result, delete_result


class RequestListApi(FlaskRestApi):
    def __init__(self, request_repo: RequestRepository, logger: Logger) -> None:
        super().__init__(logger)
        self.request_repo = request_repo
        self.logger = logger

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        all_results = self.request_repo.get_all_keys()  # type: ignore
        return ApiResponse(HttpStatusCode.ok, all_results)

    def _post(self, the_request: ApiRequest) -> ApiResponse:
        execution_request = self._parse_request(the_request)
        task_id = execution_request.uuid()
        task_result = retrieve_result(task_id)
        if task_result.status in [TaskStatus.ignored, TaskStatus.in_progress, TaskStatus.done]:
            message = "Could not send task #{}: is already in state {}".format(task_id, task_result.status)
            self.logger.warning(message)
            return ApiResponse(HttpStatusCode.precondition_failed, {"error": message})
        else:
            async_result = run_task(task=extract_feature,
                                    task_id=task_id,
                                    extraction_request=execution_request.to_serializable())
            self.logger.info("Sent feature extraction task: {} with id: {}.".format(execution_request, task_id))
            return ApiResponse(HttpStatusCode.accepted, {"task_id": async_result.task_id})

    def _parse_request(self, the_request: ApiRequest) -> ExtractionRequest:
        try:
            request_json = the_request.payload
            execution_request = ExtractionRequest.from_serializable(request_json)
            return execution_request
        except Exception as e:
            raise ClientError("Could not parse request body: {}".format(e))


class RequestDetailsApi(FlaskRestApi):
    def __init__(self, request_repo: RequestRepository, logger: Logger) -> None:
        super().__init__(logger)
        self.request_repo = request_repo
        self.logger = logger

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        try:
            task_id = the_request.query_params["task_id"]
        except Exception:
            return ApiResponse(HttpStatusCode.bad_request,
                               payload={"error": "Could not find task_id parameter in URL: {}".format(the_request.url)})
        data_model = self.request_repo.get_by_id(task_id)
        if data_model is not None:
            return ApiResponse(HttpStatusCode.ok, data_model.to_serializable())
        else:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        try:
            task_id = the_request.query_params["task_id"]
        except Exception:
            return ApiResponse(HttpStatusCode.bad_request,
                               payload={"error": "Could not find task_id parameter in URL: {}".format(the_request.url)})
        task_result = retrieve_result(task_id)
        if task_result.status in [TaskStatus.done, TaskStatus.failed]:
            try:
                self.request_repo.delete_by_id(task_id)
                delete_result(task_id)
                return ApiResponse(HttpStatusCode.ok, {"task_id": task_id})
            except Exception:
                return ApiResponse(HttpStatusCode.not_found,
                                   payload={"error": "Could not find result with id: {}".format(task_id)})
        else:
            return ApiResponse(HttpStatusCode.precondition_failed,
                               payload={"error": "Can not remove request that has not finished; status: {}".format(
                                   task_result.status.name)})


class RequestStatusApi(FlaskRestApi):
    def _get(self, the_request: ApiRequest) -> ApiResponse:
        task_id = the_request.query_params["task_id"]
        task_result = retrieve_result(task_id)
        if task_result.status in [TaskStatus.in_progress, TaskStatus.not_known, TaskStatus.ignored]:
            return ApiResponse(HttpStatusCode.no_content, None)
        else:
            return ApiResponse(HttpStatusCode.ok, task_result.to_serializable())
