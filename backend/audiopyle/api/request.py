from typing import List

from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.db.exception import EntityNotFound
from audiopyle.lib.models.result import AnalysisRequest
from audiopyle.lib.repository.request import RequestRepository
from audiopyle.lib.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode, ClientError
from audiopyle.api.utils import build_request, log_api_call, build_response
from audiopyle.lib.models.extraction_request import ExtractionRequest
from audiopyle.lib.services.metric_config_provider import MetricConfigProvider
from audiopyle.lib.services.plugin_config_provider import PluginConfigProvider
from audiopyle.worker.engine.tasks import extract_feature
from audiopyle.worker.result_model import TaskStatus
from audiopyle.worker.task_api import run_task, retrieve_result, delete_result


class RequestListApi(AbstractRestApi):
    def __init__(self, request_repo: RequestRepository, plugin_config_provider: PluginConfigProvider,
                 metric_config_provider: MetricConfigProvider) -> None:
        self.request_repo = request_repo
        self.plugin_config_provider = plugin_config_provider
        self.metric_config_provider = metric_config_provider

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        all_results = self.request_repo.get_all()  # type: List[AnalysisRequest]
        api_response = ApiResponse(HttpStatusCode.ok, [r.to_serializable() for r in all_results])
        log_api_call(api_request, api_response)
        return build_response(api_response)

    def post(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        execution_request = self._parse_request(api_request)
        task_id = execution_request.task_id
        task_result = retrieve_result(task_id)
        if task_result.status in [TaskStatus.ignored, TaskStatus.in_progress, TaskStatus.done]:
            message = "Could not send task #{}: is already in state {}".format(task_id, task_result.status)
            api_response = ApiResponse(HttpStatusCode.precondition_failed, {"message": message})
        else:
            async_result = run_task(task=extract_feature, task_id=task_id,
                                    extraction_request=execution_request.to_serializable())
            api_response = ApiResponse(HttpStatusCode.accepted, {"task_id": async_result.task_id})
        log_api_call(api_request, api_response)
        return build_response(api_response)

    def _parse_request(self, the_request: ApiRequest) -> ExtractionRequest:
        try:
            request_json = the_request.payload
            if request_json["plugin_config"] is None:
                request_json["plugin_config"] = self.plugin_config_provider.get_for_plugin(request_json["plugin_full_key"])
            if request_json["metric_config"] is None:
                request_json["metric_config"] = self.metric_config_provider.get_for_plugin(request_json["plugin_full_key"])
            execution_request = ExtractionRequest.from_serializable(request_json)
            return execution_request
        except Exception as e:
            raise ClientError("Could not parse request body: {}".format(e))


class RequestDetailsApi(AbstractRestApi):
    def __init__(self, request_repo: RequestRepository) -> None:
        self.request_repo = request_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            task_id = api_request.query_params["task_id"]
            data_model = self.request_repo.get_by_id(task_id)
            if data_model is not None:
                api_response = ApiResponse(HttpStatusCode.ok, data_model.to_serializable())
            else:
                api_response = ApiResponse(HttpStatusCode.not_found,
                                           payload={"message": "Could not find result with id: {}".format(task_id)})
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       payload={"message": "Could not find task_id parameter in URL: {}".format(
                                           api_request.url)})
        log_api_call(api_request, api_response)
        return build_response(api_response)

    def delete(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            task_id = api_request.query_params["task_id"]
            task_result = retrieve_result(task_id)
            if task_result.status in [TaskStatus.done, TaskStatus.failed]:
                self.request_repo.delete_by_id(task_id)
                delete_result(task_id)
                api_response = ApiResponse(HttpStatusCode.ok, {"task_id": task_id})
            else:
                api_response = ApiResponse(HttpStatusCode.precondition_failed,
                                           payload={
                                               "message": "Can not remove request that has not finished; status: {}".format(
                                                   task_result.status.name)})
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       payload={"message": "Could not find task_id parameter in URL: {}".format(
                                           api_request.url)})
        except EntityNotFound:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       payload={"message": "Could not find result with id: {}".format(task_id)})

        log_api_call(api_request, api_response)
        return build_response(api_response)


class RequestStatusApi(AbstractRestApi):
    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            task_id = api_request.query_params["task_id"]
            task_result = retrieve_result(task_id)
            if task_result.status == TaskStatus.not_known:
                api_response = ApiResponse(HttpStatusCode.not_found, task_result.to_serializable())
            else:
                api_response = ApiResponse(HttpStatusCode.ok, task_result.to_serializable())
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       {"message": "Parameter task_id was not provided in URL"})
        log_api_call(api_request, api_response)
        return build_response(api_response)
