import cherrypy

from commons.logger import setup_logger, get_logger
from extracter.exctracter_api import ExtracterApi, PluginApi, AudioApi

HTTP_CHERRYPY_CONFIG_FILE = "http_server.conf"
EXTRACTER_API_CONF = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher()
    }
}

if __name__ == '__main__':
    setup_logger()
    logger = get_logger()
    logger.info("Initializing Extracter app...")

    root_api = ExtracterApi(logger=logger)
    root_api.plugin = PluginApi(logger=logger)
    root_api.audio = AudioApi(logger=logger)

    cherrypy.log.error_log.propagate = False
    cherrypy.log.access_log.propagate = False
    cherrypy.config.update(HTTP_CHERRYPY_CONFIG_FILE)
    cherrypy.tree.mount(root_api, '/', EXTRACTER_API_CONF)

    logger.info("Starting Extracter API...")
    cherrypy.engine.start()
    cherrypy.engine.block()
