from commons.abstractions.api import AudiopyleRestApi
from commons.vampy.plugin_providing import list_vampy_plugins


class PluginApi(AudiopyleRestApi):
    def get(self, request_url, query_params):
        return list_vampy_plugins()
