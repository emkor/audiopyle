from logging import Logger

import cherrypy

from commons.abstractions.api_model import ApiRequest, ApiResponse, HttpMethod
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
        request = ApiRequest(url=cherrypy.url(), method=HttpMethod.GET, query_params=query_params,
                             headers=cherrypy.request.headers, payload={})
        response = self.get(request)
        response_json = to_json(response.payload)
        self._log_api_call(request, response)
        return response_json

    @cherrypy.tools.accept(media=APPLICATION_JSON_HEADER)
    @cherrypy.tools.json_in()
    def POST(self, **query_params):
        request = ApiRequest(url=cherrypy.url(), method=HttpMethod.POST, query_params=query_params,
                             headers=cherrypy.request.headers, payload=cherrypy.request.json)
        response = self.post(request)
        response_json = to_json(response.payload)
        self._log_api_call(request, response)
        return response_json

    @cherrypy.tools.accept(media=APPLICATION_JSON_HEADER)
    def PUT(self, **query_params):
        request = ApiRequest(url=cherrypy.url(), method=HttpMethod.POST, query_params=query_params,
                             headers=cherrypy.request.headers, payload=cherrypy.request.json)
        response = self.post(request)
        response_json = to_json(response)
        self._log_api_call(request, response)
        return response_json

    @cherrypy.tools.accept(media=TEXT_PLAIN_HEADER)
    def DELETE(self, **query_params):
        request = ApiRequest(url=cherrypy.url(), method=HttpMethod.POST, query_params=query_params,
                             headers=cherrypy.request.headers, payload=cherrypy.request.json)
        response = self.delete(request)
        response_json = to_json(response)
        self._log_api_call(request, response)
        return response_json

    def _log_api_call(self, api_request: ApiRequest, api_response: ApiResponse):
        serving_time = seconds_between(api_request.creation_time)
        self.logger.debug("{} served {} on {} with {} in {}s.".format(self.__class__.__name__, api_request.method,
                                                                      api_request.url, api_response.status_code.name,
                                                                      serving_time))
