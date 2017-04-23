from commons.model import Model


class ExtractionRequest(Model):
    def __init__(self, audio_file, plugin_key, plugin_output):
        """
        :type audio_file: str
        :type plugin_key: str
        :type plugin_output: str
        """
        self.plugin_output = plugin_output
        self.plugin_key = plugin_key
        self.audio_file = audio_file
