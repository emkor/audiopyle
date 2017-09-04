from logging import Logger
from typing import Optional, Any, Text, Dict, Callable

import cherrypy

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpMethod, ClientError, ServerError
from commons.utils.conversion import seconds_between
from commons.utils.logger import get_logger
from commons.utils.serialization import to_json

TEXT_PLAIN_HEADER = 'text/plain'
APPLICATION_JSON_HEADER = 'application/json'


class AudiopyleRestApi(object):
    exposed = True

    def __init__(self, logger: Logger = None) -> None:
        self.not_implemented_api_method = cherrypy.HTTPError(405, 'Method Not Allowed')
        self.logger = logger or get_logger()

    def get(self, request: ApiRequest) -> ApiResponse:
        raise self.not_implemented_api_method

    def post(self, request: ApiRequest) -> ApiResponse:
        raise self.not_implemented_api_method

    def put(self, request: ApiRequest) -> ApiResponse:
        raise self.not_implemented_api_method

    def delete(self, request: ApiRequest) -> ApiResponse:
        raise self.not_implemented_api_method

    @cherrypy.tools.accept(media=TEXT_PLAIN_HEADER)
    def GET(self, **query_params):
        return self._handle_request(cherrypy.url(), HttpMethod.GET, self.get, query_params,
                                    cherrypy.request.headers, None)

    @cherrypy.tools.accept(media=APPLICATION_JSON_HEADER)
    @cherrypy.tools.json_in()
    def POST(self, **query_params):
        return self._handle_request(cherrypy.url(), HttpMethod.POST, self.post, query_params,
                                    cherrypy.request.headers, cherrypy.request.json)

    @cherrypy.tools.accept(media=APPLICATION_JSON_HEADER)
    def PUT(self, **query_params):
        return self._handle_request(cherrypy.url(), HttpMethod.PUT, self.put, query_params,
                                    cherrypy.request.headers, cherrypy.request.json)

    @cherrypy.tools.accept(media=TEXT_PLAIN_HEADER)
    def DELETE(self, **query_params):
        return self._handle_request(cherrypy.url(), HttpMethod.DELETE, self.delete, query_params,
                                    cherrypy.request.headers, None)

    def _handle_request(self,
                        request_url: Text,
                        http_method: HttpMethod,
                        method_handler: Callable[..., ApiResponse],
                        query_params: Dict[Text, Any],
                        headers: Dict[Text, Any],
                        request_payload: Optional[Dict[Text, Any]] = None):
        request = ApiRequest(url=request_url, method=http_method, query_params=query_params,
                             headers=headers, payload=request_payload or {})
        try:
            response = method_handler(request)
            response_json = to_json(response.payload)
            self._log_api_call(request, response)
            return response_json
        except ClientError as e:
            self.logger.warning("Bad request to {}: {}, request: {}".format(self.__class__.__name__, e, request))
            raise cherrypy.HTTPError(status=e.status_code, message=e.message)
        except Exception as e:
            self.logger.exception("Server error in {}: {}, request: {}".format(self.__class__.__name__, e, request))
            raise cherrypy.HTTPError(status=500, message=e)

    def _log_api_call(self, api_request: ApiRequest, api_response: ApiResponse):
        serving_time = seconds_between(api_request.creation_time)
        self.logger.debug("{} served {} on {} with {} in {}s.".format(self.__class__.__name__, api_request.method,
                                                                      api_request.url, api_response.status_code.name,
                                                                      serving_time))
