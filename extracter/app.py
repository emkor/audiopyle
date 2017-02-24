import cherrypy

from commons.logger import setup_logger
from extracter.exctracter_api import ExtracterApi, PluginApi, AudioApi

HTTP_CHERRYPY_CONFIG_FILE = "http_server.conf"
EXTRACTER_API_CONF = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher()
    }
}

if __name__ == '__main__':
    setup_logger()
    root_api = ExtracterApi()
    root_api.plugin = PluginApi()
    root_api.audio = AudioApi()

    cherrypy.config.update(HTTP_CHERRYPY_CONFIG_FILE)
    cherrypy.tree.mount(root_api, '/', EXTRACTER_API_CONF)

    cherrypy.engine.start()
    cherrypy.engine.block()
