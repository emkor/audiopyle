from logging import Logger

from audiopyle.lib.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from audiopyle.lib.abstractions.flask_api import FlaskRestApi
from audiopyle.lib.db.exception import EntityNotFound
from audiopyle.lib.repository.feature_data import FeatureDataRepository
from audiopyle.lib.repository.stats import ResultStatsRepository
from audiopyle.lib.services.compression import from_compressed_feature


class ResultDataApi(FlaskRestApi):
    def __init__(self, feature_data_repo: FeatureDataRepository, logger: Logger) -> None:
        super().__init__(logger)
        self.feature_data_repo = feature_data_repo
        self.logger = logger

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        try:
            task_id = the_request.query_params["task_id"]
        except Exception:
            return ApiResponse(HttpStatusCode.bad_request,
                               payload={"error": "Could not find task_id parameter in URL: {}".format(the_request.url)})
        data_entity = self.feature_data_repo.get_by_id(task_id)
        if data_entity is not None:
            vampy_feature = from_compressed_feature(data_entity)
            return ApiResponse(HttpStatusCode.ok, vampy_feature.to_serializable())
        else:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        try:
            task_id = the_request.query_params["task_id"]
        except Exception:
            return ApiResponse(HttpStatusCode.bad_request,
                               payload={"error": "Could not find task_id parameter in URL: {}".format(the_request.url)})
        try:
            self.feature_data_repo.delete_by_id(task_id)
            return ApiResponse(HttpStatusCode.ok, None)
        except EntityNotFound:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})


class ResultMetaApi(FlaskRestApi):
    def __init__(self, feature_meta_repo: FeatureDataRepository, logger: Logger) -> None:
        super().__init__(logger)
        self.feature_meta_repo = feature_meta_repo
        self.logger = logger

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        try:
            task_id = the_request.query_params["task_id"]
        except Exception:
            return ApiResponse(HttpStatusCode.bad_request,
                               payload={"error": "Could not find task_id parameter in URL: {}".format(the_request.url)})
        data_entity = self.feature_meta_repo.get_by_id(task_id)
        if data_entity is not None:
            return ApiResponse(HttpStatusCode.ok, data_entity.to_serializable())
        else:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        try:
            task_id = the_request.query_params["task_id"]
        except Exception:
            return ApiResponse(HttpStatusCode.bad_request,
                               payload={"error": "Could not find task_id parameter in URL: {}".format(the_request.url)})
        try:
            self.feature_meta_repo.delete_by_id(task_id)
            return ApiResponse(HttpStatusCode.ok, None)
        except EntityNotFound:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})


class ResultStatsApi(FlaskRestApi):
    def __init__(self, stats_repo: ResultStatsRepository, logger: Logger) -> None:
        super().__init__(logger)
        self.stats_repo = stats_repo
        self.logger = logger

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        try:
            task_id = the_request.query_params["task_id"]
            data_entity = self.stats_repo.get_by_id(task_id)
            if data_entity:
                return ApiResponse(HttpStatusCode.ok, data_entity.to_serializable())
            else:
                return ApiResponse(HttpStatusCode.not_found,
                                   payload={"error": "Could not find stats with id: {}".format(task_id)})
        except KeyError:
            return ApiResponse(HttpStatusCode.bad_request,
                               payload={"error": "Could not find task_id parameter in URL: {}".format(the_request.url)})
        except EntityNotFound:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        try:
            task_id = the_request.query_params["task_id"]
        except Exception:
            return ApiResponse(HttpStatusCode.bad_request,
                               payload={"error": "Could not find task_id parameter in URL: {}".format(the_request.url)})
        try:
            self.stats_repo.delete_by_id(task_id)
            return ApiResponse(HttpStatusCode.ok, None)
        except EntityNotFound:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})
