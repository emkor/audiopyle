from commons.model import Model


class ExtractionRequest(Model):
    def __init__(self, audio_file_name, plugin_key, plugin_output):
        """
        :type audio_file_name: str
        :type plugin_key: str
        :type plugin_output: str
        """
        self.audio_file_name = audio_file_name
        self.plugin_key = plugin_key
        self.plugin_output = plugin_output
