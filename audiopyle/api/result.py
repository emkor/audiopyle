from flask import request

from audiopyle.lib.abstractions.api import AbstractRestApi
from audiopyle.lib.abstractions.api_model import ApiResponse, HttpStatusCode
from audiopyle.api.utils import build_request, log_api_call, build_response
from audiopyle.lib.db.exception import EntityNotFound
from audiopyle.lib.repository.feature_data import FeatureDataRepository
from audiopyle.lib.repository.feature_meta import FeatureMetaRepository
from audiopyle.lib.repository.stats import ResultStatsRepository
from audiopyle.lib.services.compression import from_compressed_feature


class ResultDataApi(AbstractRestApi):
    def __init__(self, feature_data_repo: FeatureDataRepository) -> None:
        self.feature_data_repo = feature_data_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            task_id = api_request.query_params["task_id"]
            data_entity = self.feature_data_repo.get_by_id(task_id)
            if data_entity is not None:
                vampy_feature = from_compressed_feature(data_entity)
                api_response = ApiResponse(HttpStatusCode.ok, vampy_feature.to_serializable())
            else:
                api_response = ApiResponse(HttpStatusCode.not_found,
                                           payload={"error": "Could not find result with id: {}".format(task_id)})
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       payload={"error": "Could not find task_id parameter in URL: {}".format(
                                           api_request.url)})
        log_api_call(api_request, api_response)
        return build_response(api_response)

    def delete(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            task_id = api_request.query_params["task_id"]
            self.feature_data_repo.delete_by_id(task_id)
            api_response = ApiResponse(HttpStatusCode.ok, None)
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       payload={"error": "Could not find task_id parameter in URL: {}".format(
                                           api_request.url)})
        except EntityNotFound:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       payload={"error": "Could not find result with id: {}".format(task_id)})
        log_api_call(api_request, api_response)
        return build_response(api_response)


class ResultMetaApi(AbstractRestApi):
    def __init__(self, feature_meta_repo: FeatureMetaRepository) -> None:
        self.feature_meta_repo = feature_meta_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            task_id = api_request.query_params["task_id"]
            data_entity = self.feature_meta_repo.get_by_id(task_id)
            if data_entity is not None:
                api_response = ApiResponse(HttpStatusCode.ok, data_entity.to_serializable())
            else:
                api_response = ApiResponse(HttpStatusCode.not_found,
                                           payload={"error": "Could not find result with id: {}".format(task_id)})
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       payload={"error": "Could not find task_id parameter in URL: {}".format(
                                           api_request.url)})
        log_api_call(api_request, api_response)
        return build_response(api_response)

    def delete(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            task_id = api_request.query_params["task_id"]
            self.feature_meta_repo.delete_by_id(task_id)
            api_response = ApiResponse(HttpStatusCode.ok, None)
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       payload={"error": "Could not find task_id parameter in URL: {}".format(
                                           api_request.url)})
        except EntityNotFound:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       payload={"error": "Could not find result with id: {}".format(task_id)})
        log_api_call(api_request, api_response)
        return build_response(api_response)


class ResultStatsApi(AbstractRestApi):
    def __init__(self, stats_repo: ResultStatsRepository) -> None:
        self.stats_repo = stats_repo

    def get(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            task_id = api_request.query_params["task_id"]
            data_entity = self.stats_repo.get_by_id(task_id)
            if data_entity:
                api_response = ApiResponse(HttpStatusCode.ok, data_entity.to_serializable())
            else:
                api_response = ApiResponse(HttpStatusCode.not_found,
                                           payload={"error": "Could not find stats with id: {}".format(task_id)})
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       payload={"error": "Could not find task_id parameter in URL: {}".format(
                                           api_request.url)})
        except EntityNotFound:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       payload={"error": "Could not find result with id: {}".format(task_id)})
        log_api_call(api_request, api_response)
        return build_response(api_response)

    def delete(self, **kwargs) -> str:
        api_request = build_request(request, **kwargs)
        try:
            task_id = api_request.query_params["task_id"]
            self.stats_repo.delete_by_id(task_id)
            api_response = ApiResponse(HttpStatusCode.ok, None)
        except KeyError:
            api_response = ApiResponse(HttpStatusCode.bad_request,
                                       payload={"error": "Could not find task_id parameter in URL: {}".format(
                                           api_request.url)})
        except EntityNotFound:
            api_response = ApiResponse(HttpStatusCode.not_found,
                                       payload={"error": "Could not find result with id: {}".format(task_id)})
        log_api_call(api_request, api_response)
        return build_response(api_response)
