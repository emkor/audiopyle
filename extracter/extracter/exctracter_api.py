import cherrypy

from commons.api_utils import to_json
from commons.file_system import list_files
from extracter.vampy_plugin_provider import list_vampy_plugins

AUDIO_FILES_DIR = "/audio"
TMP_DIR = "/audio_tmp"


class ExtracterApi(object):
    @cherrypy.expose
    def index(self):
        """
        :rtype: str
        """
        return to_json({"api": "extracter", "status": "ok"})

    @cherrypy.expose
    def plugins(self):
        """
        :rtype: str
        """
        return to_json(list_vampy_plugins())

    @cherrypy.expose
    def audio(self):
        """
        :rtype: str
        """
        return to_json(list_files(AUDIO_FILES_DIR))
