import abc
import cherrypy

from commons.logger import get_logger
from commons.serializer import to_json


class AudiopyleRestApi(object):
    exposed = True

    def __init__(self, logger=None):
        """
        :type logger: logging.Logger
        """
        self.not_implemented_api_method = cherrypy.HTTPError(405, 'Method Not Allowed')
        self.logger = logger or get_logger()

    @abc.abstractmethod
    def get(self, request_url, query_params):
        """
        :type request_url: str
        :type query_params: dict[str, str]
        :rtype: basestring | int | float | list | dict | None
        """
        raise self.not_implemented_api_method

    @abc.abstractmethod
    def post(self, request_url, query_params, request_payload):
        """
        :type request_url: str
        :type query_params: dict
        :type request_payload: dict
        :rtype: basestring | int | float | list | dict | None
        """
        raise self.not_implemented_api_method

    @abc.abstractmethod
    def put(self, request_url, query_params, request_payload):
        """
        :type request_url: str
        :type query_params: dict
        :type request_payload: dict
        :rtype: basestring | int | float | list | dict | None
        """
        raise self.not_implemented_api_method

    @abc.abstractmethod
    def delete(self, request_url, query_params):
        """
        :type request_url: str
        :type query_params: dict
        :rtype: basestring | int | float | list | dict | None
        """
        raise self.not_implemented_api_method

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, **query_params):
        request_url = cherrypy.url()
        response_json = to_json(self.get(request_url=request_url, query_params=query_params))
        self._log_api_call("GET", request_url, response_json)
        return response_json

    @cherrypy.tools.accept(media='application/json')
    @cherrypy.tools.json_in()
    def POST(self, **query_params):
        request_url = cherrypy.url()
        request_json = cherrypy.request.json
        response_json = to_json(
            self.post(request_url=request_url, query_params=query_params, request_payload=request_json))
        self._log_api_call("POST", request_url, response_json, request_json)
        return response_json

    @cherrypy.tools.accept(media='application/json')
    def PUT(self, **query_params):
        request_url = cherrypy.url()
        request_json = cherrypy.request.json
        response_json = to_json(
            self.post(request_url=request_url, query_params=query_params, request_payload=request_json))
        self._log_api_call("PUT", request_url, response_json, request_json)
        return response_json

    @cherrypy.tools.accept(media='text/plain')
    def DELETE(self, **query_params):
        request_url = cherrypy.url()
        response_json = to_json(self.delete(request_url=request_url, query_params=query_params))
        self._log_api_call("DELETE", request_url, response_json)
        return response_json

    def _log_api_call(self, method_name, request_url, response_json, request_json=None):
        """
        :type method_name: str
        :type request_url: str
        :type response_json: str
        :type request_json: str
        """
        self.logger.debug(
            "{} on {} at {} with payload {} and response {}".format(method_name, self.__class__.__name__, request_url,
                                                                    request_json, response_json))
