from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode
from audiopyle.api.utils import build_request, log_api_call, build_response
from audiopyle.lib.repository.metric import MetricDefinitionRepository, MetricValueRepository


class MetricDefinitionListApi(AbstractRestApi):
    def __init__(self, metric_repo: MetricDefinitionRepository) -> None:
        self.metric_repo = metric_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        all_results = self.metric_repo.get_all_keys()  # type: ignore
        api_response = ApiResponse(HttpStatusCode.ok, all_results)
        log_api_call(api_request, api_response)
        return build_response(api_response)


class MetricDefinitionDetailsApi(AbstractRestApi):
    def __init__(self, metric_repo: MetricDefinitionRepository) -> None:
        self.metric_repo = metric_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            metric_def_id = api_request.query_params["id"]
            metric_definition = self.metric_repo.get_by_id(metric_def_id)
            if metric_definition:
                api_response = ApiResponse(status_code=HttpStatusCode.ok, payload=metric_definition.to_serializable())
            else:
                api_response = ApiResponse(status_code=HttpStatusCode.not_found,
                                           payload={
                                               "Could not find metric definition with id: {}".format(metric_def_id)})
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       {"error": "Could not find metric definition ID in URL: {}".format(
                                           api_request.url)})
        log_api_call(api_request, api_response)
        return build_response(api_response)


class MetricValueListApi(AbstractRestApi):
    def __init__(self, metric_repo: MetricValueRepository) -> None:
        self.metric_repo = metric_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        all_results = self.metric_repo.get_all_keys()  # type: ignore
        api_response = ApiResponse(HttpStatusCode.ok, all_results)
        log_api_call(api_request, api_response)
        return build_response(api_response)


class MetricValueDetailsApi(AbstractRestApi):
    def __init__(self, metric_repo: MetricValueRepository) -> None:
        self.metric_repo = metric_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            metric_def_id = api_request.query_params["id"]
            metric_definition = self.metric_repo.get_by_id(metric_def_id)
            if metric_definition is not None:
                api_response = ApiResponse(status_code=HttpStatusCode.ok, payload=metric_definition.to_serializable())
            else:
                api_response = ApiResponse(status_code=HttpStatusCode.not_found,
                                           payload={
                                               "error": "Could not find metric value with ID of {}".format(
                                                   metric_def_id)})
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       {"error": "Could not find metric value ID in URL: {}".format(api_request.url)})
        log_api_call(api_request, api_response)
        return build_response(api_response)
