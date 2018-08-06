from logging import Logger

from audiopyle.commons.abstractions.api_model import ApiRequest, ApiResponse, MethodNotSupportedError
from audiopyle.commons.utils.conversion import seconds_between
from audiopyle.commons.utils.logger import get_logger


class AbstractRestApi(object):
    def __init__(self, logger: Logger = None) -> None:
        self.logger = logger or get_logger()

    def _get(self, the_request: ApiRequest) -> ApiResponse:
        raise MethodNotSupportedError("{} does not support GET at {}".format(self.__class__.__name__, the_request.url))

    def _post(self, the_request: ApiRequest) -> ApiResponse:
        raise MethodNotSupportedError("{} does not support POST at {}".format(self.__class__.__name__, the_request.url))

    def _put(self, the_request: ApiRequest) -> ApiResponse:
        raise MethodNotSupportedError("{} does not support PUT at {}".format(self.__class__.__name__, the_request.url))

    def _delete(self, the_request: ApiRequest) -> ApiResponse:
        raise MethodNotSupportedError(
            "{} does not support DELETE at {}".format(self.__class__.__name__, the_request.url))

    def _log_api_call(self, api_request: ApiRequest, api_response: ApiResponse):
        serving_time = seconds_between(api_request.creation_time)
        self.logger.info("{} served {} at {} with {} ({} -> {}) in {}s.".format(self.__class__.__name__,
                                                                                api_request.method,
                                                                                api_request.url,
                                                                                api_response.status_code,
                                                                                api_request.size_humanized(),
                                                                                api_response.size_humanized(),
                                                                                serving_time))
