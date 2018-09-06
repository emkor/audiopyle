from typing import List

from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode
from audiopyle.api.utils import build_request, log_api_call, build_response
from audiopyle.lib.models.metric import MetricDefinition
from audiopyle.lib.repository.metric import MetricDefinitionRepository, MetricValueRepository


class MetricDefinitionListApi(AbstractRestApi):
    def __init__(self, metric_repo: MetricDefinitionRepository) -> None:
        self.metric_repo = metric_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        all_definitions = self.metric_repo.get_all()  # type: List[MetricDefinition]
        api_response = ApiResponse(HttpStatusCode.ok, [d.to_serializable() for d in all_definitions])
        log_api_call(api_request, api_response)
        return build_response(api_response)


class MetricDefinitionDetailsApi(AbstractRestApi):
    def __init__(self, metric_repo: MetricDefinitionRepository) -> None:
        self.metric_repo = metric_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            metric_name = api_request.query_params["name"]
            metric_definition = self.metric_repo.get_metric_by_name(metric_name)
            if metric_definition:
                api_response = ApiResponse(status_code=HttpStatusCode.ok, payload=metric_definition.to_serializable())
            else:
                api_response = ApiResponse(status_code=HttpStatusCode.not_found,
                                           payload={
                                               "Could not find metric definition named: {}".format(metric_name)})
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       {"message": "Could not find metric definition name in URL: {}".format(
                                           api_request.url)})
        log_api_call(api_request, api_response)
        return build_response(api_response)


class MetricValueListApi(AbstractRestApi):
    def __init__(self, metric_repo: MetricValueRepository) -> None:
        self.metric_repo = metric_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        definition_name = api_request.query_params.get("name")
        task_id = api_request.query_params.get("task_id")
        if definition_name is None and task_id is None:
            message = "Could not find either metric definition name or task_id in URL: {}".format(api_request.url)
            api_response = ApiResponse(HttpStatusCode.bad_request, {"message": message})
        elif definition_name is not None:
            values = self.metric_repo.get_values_by_name(metric_name=definition_name)
            if values is None:
                api_response = ApiResponse(HttpStatusCode.not_found, {
                    "message": "Could not find metric definition named {}".format(definition_name)})
            else:
                api_response = ApiResponse(HttpStatusCode.ok, [v.task_id for v in values])
        elif task_id is not None:
            values = self.metric_repo.get_by_task_id(task_id=task_id)
            api_response = ApiResponse(HttpStatusCode.ok, [v.definition.name for v in values])
        else:
            api_response = ApiResponse(HttpStatusCode.bad_request, {
                "message": "Listing API does not support querying by task_id and metric name at the same time"})
        log_api_call(api_request, api_response)
        return build_response(api_response)


class MetricValueDetailsApi(AbstractRestApi):
    def __init__(self, metric_repo: MetricValueRepository) -> None:
        self.metric_repo = metric_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            metric_def_name = api_request.query_params["name"]
            task_id = api_request.query_params["task_id"]
            metric_definition = self.metric_repo.get_by_name_and_task_id(metric_name=metric_def_name,
                                                                         task_id=task_id)
            if metric_definition is not None:
                api_response = ApiResponse(status_code=HttpStatusCode.ok, payload=metric_definition.to_serializable())
            else:
                message = "Could not find metric value for definition named {} with task_id {}".format(
                    metric_def_name, task_id)
                api_response = ApiResponse(status_code=HttpStatusCode.not_found, payload={"message": message})
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       {"message": "Could not find metric definition name or task_id in URL: {}".format(
                                           api_request.url)})
        log_api_call(api_request, api_response)
        return build_response(api_response)
