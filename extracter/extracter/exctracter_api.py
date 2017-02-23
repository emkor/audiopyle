import json
import cherrypy

from extracter.vampy_plugin_provider import list_vampy_plugins


class ExtracterApi(object):
    @cherrypy.expose
    def index(self):
        return json.dumps({"api": "extracter", "status": "ok"})

    @cherrypy.expose
    def plugins(self):
        """
        :rtype: str
        """
        return json.dumps(list_vampy_plugins())

    @cherrypy.expose
    def files(self):
        """
        :return:
        :rtype:
        """
        return ""
