import cherrypy

from commons.api_utils import jsonify
from commons.file_system import list_files
from extracter.vampy_plugin_provider import list_vampy_plugins

AUDIO_FILES_DIR = "/audio"
TMP_DIR = "/audio_tmp"


class ExtracterApi(object):
    @cherrypy.expose
    @jsonify
    def index(self):
        """
        :rtype: str
        """
        return {"api": "extracter", "status": "ok"}

    @cherrypy.expose
    @jsonify
    def plugins(self):
        """
        :rtype: str
        """
        return list_vampy_plugins()

    @cherrypy.expose
    @jsonify
    def audio(self):
        """
        :rtype: str
        """
        return list_files(AUDIO_FILES_DIR)
