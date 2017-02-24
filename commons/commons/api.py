import abc
import cherrypy

from commons.serializer import to_json


class AudiopyleApi(object):
    exposed = True
    NOT_IMPLEMENTED_API_METHOD = cherrypy.HTTPError(405, 'Method Not Allowed')

    @abc.abstractmethod
    def get(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD

    @abc.abstractmethod
    def post(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD

    @abc.abstractmethod
    def put(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD

    @abc.abstractmethod
    def delete(self, *args, **kwargs):
        raise self.NOT_IMPLEMENTED_API_METHOD

    @cherrypy.tools.accept(media='text/plain')
    def GET(self, *args, **kwargs):
        json = to_json(self.get(*args, **kwargs))
        print("GET args: {} kwargs: {} output: {}").format(args, kwargs, json)
        return json

    @cherrypy.tools.accept(media='application/json')
    def POST(self, *args, **kwargs):
        json = to_json(self.post(*args, **kwargs))
        print("POST args: {} kwargs: {} output: {}").format(args, kwargs, json)
        return json

    @cherrypy.tools.accept(media='application/json')
    def PUT(self, *args, **kwargs):
        json = to_json(self.put(*args, **kwargs))
        print("PUT args: {} kwargs: {} output: {}").format(args, kwargs, json)
        return json

    @cherrypy.tools.accept(media='text/plain')
    def DELETE(self, *args, **kwargs):
        json = to_json(self.delete(*args, **kwargs))
        print("DELETE args: {} kwargs: {} output: {}").format(args, kwargs, json)
        return json
