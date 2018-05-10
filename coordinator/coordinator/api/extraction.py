from logging import Logger

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from commons.models.extraction_request import ExtractionRequest
from commons.services.metric_config_provider import MetricConfigProvider
from commons.services.plugin_config_provider import PluginConfigProvider
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
    def __init__(self, plugin_config_provider: PluginConfigProvider, metric_config_provider: MetricConfigProvider,logger: Logger) -> None:
        super().__init__(logger)
        self.plugin_config_provider = plugin_config_provider
        self.metric_config_provider = metric_config_provider

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
        request_json = the_request.payload
        plugin_config = self.plugin_config_provider.get_for_plugin(request_json["plugin_full_key"])
        metric_config = self.metric_config_provider.get_for_plugin(request_json["plugin_full_key"])
        request_json.update({"plugin_config": plugin_config,
                             "metric_config": metric_config})
        execution_request = ExtractionRequest.from_serializable(request_json)
        return execution_request
