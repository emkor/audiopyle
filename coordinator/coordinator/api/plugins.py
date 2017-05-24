from commons.abstractions.api import AudiopyleRestApi
from commons.vampy.plugin_providing import list_vampy_plugins


class PluginApi(AudiopyleRestApi):
    def get(self, request_url, query_params):
        return list_vampy_plugins()

    def post(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method

    def delete(self, request_url, query_params):
        raise self.not_implemented_api_method

    def put(self, request_url, query_params, request_payload):
        raise self.not_implemented_api_method
