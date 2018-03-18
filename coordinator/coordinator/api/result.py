from logging import Logger

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from commons.abstractions.flask_api import FlaskRestApi
from commons.db.exception import EntityNotFound
from commons.repository.feature_data import FeatureDataRepository
from commons.repository.result import ResultRepository, ResultStatsRepository
from commons.services.compression import from_compressed_feature


class ResultListApi(FlaskRestApi):
    def __init__(self, result_repo: ResultRepository, logger: Logger) -> None:
        super().__init__(logger)
        self.result_repo = result_repo
        self.logger = logger

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        all_results = self.result_repo.get_all()
        return ApiResponse(HttpStatusCode.ok, all_results)


class ResultDataApi(FlaskRestApi):
    def __init__(self, feature_data_repo: FeatureDataRepository, logger: Logger) -> None:
        super().__init__(logger)
        self.feature_data_repo = feature_data_repo
        self.logger = logger

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        task_id = the_request.query_params.get("task_id")
        try:
            data_entity = self.feature_data_repo.get_by_id(task_id)
            vampy_feature = from_compressed_feature(data_entity)
            return ApiResponse(HttpStatusCode.ok, vampy_feature.to_serializable())
        except EntityNotFound:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        task_id = the_request.query_params.get("task_id")
        try:
            entity_id = self.feature_data_repo.get_by_id(task_id)
            self.feature_data_repo.delete_by_id(entity_id)
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
        task_id = the_request.query_params.get("task_id")
        try:
            data_entity = self.feature_meta_repo.get_by_id(task_id)
            return ApiResponse(HttpStatusCode.ok, data_entity.to_serializable())
        except EntityNotFound:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        task_id = the_request.query_params.get("task_id")
        try:
            entity_id = self.feature_meta_repo.get_by_id(task_id)
            self.feature_meta_repo.delete_by_id(entity_id)
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
        task_id = the_request.query_params.get("task_id")
        try:
            data_entity = self.stats_repo.get_by_id(task_id)
            return ApiResponse(HttpStatusCode.ok, data_entity.to_serializable())
        except EntityNotFound:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        task_id = the_request.query_params.get("task_id")
        try:
            entity_id = self.stats_repo.get_by_id(task_id)
            self.stats_repo.delete_by_id(entity_id)
            return ApiResponse(HttpStatusCode.ok, None)
        except EntityNotFound:
            return ApiResponse(HttpStatusCode.not_found,
                               payload={"error": "Could not find result with id: {}".format(task_id)})
