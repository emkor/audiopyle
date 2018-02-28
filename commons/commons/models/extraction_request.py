from typing import Text

from commons.abstractions.model import Model
from commons.services.uuid_generation import generate_uuid


class ExtractionRequest(Model):
    def __init__(self, audio_file_name: Text, plugin_key: Text, plugin_output: Text) -> None:
        self.audio_file_name = audio_file_name
        self.plugin_key = plugin_key
        self.plugin_output = plugin_output

    def uuid(self) -> Text:
        return generate_uuid("{};{};{}".format(self.audio_file_name, self.plugin_key, self.plugin_output))
