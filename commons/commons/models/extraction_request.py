from typing import Text, Any, Dict

from commons.abstractions.model import Model
from commons.services.uuid_generation import generate_uuid


class ExtractionRequest(Model):
    def __init__(self, audio_file_name: Text, plugin_full_key: Text, plugin_config: Dict[Text, Any],
                 metric_config: Dict[Text, Any]) -> None:
        self.audio_file_name = audio_file_name
        self.plugin_full_key = plugin_full_key
        self.plugin_config = plugin_config
        self.metric_config = metric_config

    def uuid(self) -> Text:
        return generate_uuid("{};{}".format(self.audio_file_name, self.plugin_full_key))
