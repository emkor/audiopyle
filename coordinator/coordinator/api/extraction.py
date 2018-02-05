from commons.abstractions.api import AudiopyleRestApi
from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode, ClientError
from commons.services.feature_extraction import ExtractionRequest
from commons.services.uuid_generation import generate_uuid
from extractor.service import run_task, retrieve_result, delete_result
from extractor.tasks import extract_feature

NO_TASK_ID_IN_QUERY_PARAM = ClientError("Bad request: did not found task_id query param")


class ExtractionApi(AudiopyleRestApi):
    def get(self, request: ApiRequest) -> ApiResponse:
        task_id = request.query_params.get("task_id")
        if task_id is not None:
            self.logger.info("Querying result of {}...".format(task_id))
            extraction_result = retrieve_result(task_id)
            self.logger.info("Returning result of {}: {}".format(task_id, extraction_result.status))
            return ApiResponse(HttpStatusCode.ok, extraction_result.to_serializable())
        else:
            raise NO_TASK_ID_IN_QUERY_PARAM

    def post(self, request: ApiRequest) -> ApiResponse:
        execution_request = ExtractionRequest.from_serializable(request.payload)
        self.logger.info("Sending feature extraction task: {}...".format(execution_request))
        serialized_request = execution_request.to_serializable()
        task_id = generate_uuid(serialized_request)
        async_result = run_task(task=extract_feature,
                                task_id=task_id,
                                extraction_request=serialized_request)
        self.logger.info("Sent feature extraction task! ID: {}.".format(async_result.task_id))
        return ApiResponse(HttpStatusCode.accepted, {"task_id": async_result.task_id})

    def delete(self, request: ApiRequest) -> ApiResponse:
        task_id = request.query_params.get("task_id")
        if task_id is not None:
            was_successful = delete_result(task_id)
            if was_successful:
                return ApiResponse(HttpStatusCode.ok, {"task_id": task_id})
            else:
                raise ClientError("Did not find result with given task id: {}".format(task_id),
                                  HttpStatusCode.bad_request)
        else:
            raise NO_TASK_ID_IN_QUERY_PARAM
