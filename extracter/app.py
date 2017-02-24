import cherrypy

from extracter.exctracter_api import ExtracterApi, PluginsApi, AudioApi

HTTP_CHERRYPY_CONFIG_FILE = "http_server.conf"

if __name__ == '__main__':
    root_conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher()
        }
    }
    cherrypy.config.update(HTTP_CHERRYPY_CONFIG_FILE)

    cherrypy.tree.mount(ExtracterApi(), '/', root_conf)
    cherrypy.tree.mount(PluginsApi(), '/plugin', root_conf)
    cherrypy.tree.mount(AudioApi(), '/audio', root_conf)

    cherrypy.engine.start()
    cherrypy.engine.block()
