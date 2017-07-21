import cherrypy

from commons.utils.logger import setup_logger, get_logger
from coordinator.api.audio import AudioApi
from coordinator.api.plugin import PluginApi
from coordinator.api.root import CoordinatorApi
from coordinator.api.extraction import ExtractionApi

HTTP_CHERRYPY_CONFIG_FILE = "http_server.conf"
COORDINATOR_API_CONF = {
    '/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher()
    }
}

if __name__ == '__main__':
    setup_logger()
    logger = get_logger()
    logger.info("Initializing Coordinator app...")

    root_api = CoordinatorApi(logger=logger)
    root_api.plugin = PluginApi(logger=logger)
    root_api.audio = AudioApi(logger=logger)
    root_api.extraction = ExtractionApi(logger=logger)

    cherrypy.log.error_log.propagate = False
    cherrypy.log.access_log.propagate = False
    cherrypy.config.update(HTTP_CHERRYPY_CONFIG_FILE)
    cherrypy.tree.mount(root_api, '/', COORDINATOR_API_CONF)

    logger.info("Starting Coordinator API...")
    cherrypy.engine.start()
    cherrypy.engine.block()
