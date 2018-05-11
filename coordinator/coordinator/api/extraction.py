from logging import Logger

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode, ClientError
from commons.abstractions.flask_api import FlaskRestApi
from commons.models.extraction_request import ExtractionRequest
from extractor.engine.tasks import extract_feature
from extractor.result_model import TaskStatus
from extractor.task_api import run_task, retrieve_result, delete_result


class ExtractionStatusApi(FlaskRestApi):
    def _get(self, the_request: ApiRequest) -> ApiResponse:
        task_id = the_request.query_params.get("task_id")
        task_result = retrieve_result(task_id)
        if task_result.status in [TaskStatus.in_progress, TaskStatus.not_known, TaskStatus.ignored]:
            return ApiResponse(HttpStatusCode.no_content, task_result.to_serializable())
        else:
            return ApiResponse(HttpStatusCode.ok, task_result.to_serializable())

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        task_id = the_request.query_params.get("task_id")
        delete_result(task_id)
        return ApiResponse(HttpStatusCode.ok, {"task_id": task_id})


class ExtractionApi(FlaskRestApi):
    def __init__(self, logger: Logger) -> None:
        super().__init__(logger)

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
