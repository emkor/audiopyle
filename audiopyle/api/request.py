from logging import Logger

from audiopyle.lib.abstractions.api_model import ApiRequest, ApiResponse, HttpStatusCode
from audiopyle.lib.abstractions.flask_api import FlaskRestApi
from audiopyle.lib.repository.request import RequestRepository


class RequestListApi(FlaskRestApi):
    def __init__(self, request_repo: RequestRepository, logger: Logger) -> None:
        super().__init__(logger)
        self.request_repo = request_repo
        self.logger = logger

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        all_results = self.request_repo.get_all_keys()  # type: ignore
        return ApiResponse(HttpStatusCode.ok, all_results)


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
