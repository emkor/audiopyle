from typing import Any, Dict, Optional

from audiopyle.lib.abstractions.model import Model
from audiopyle.lib.services.uuid_generation import generate_uuid


class ExtractionRequest(Model):
    def __init__(self, audio_file_name: str, plugin_full_key: str,
                 plugin_config: Optional[Dict[str, Any]] = None,
                 metric_config: Optional[Dict[str, Any]] = None) -> None:
        self.audio_file_name = audio_file_name
        self.plugin_full_key = plugin_full_key
        self.plugin_config = plugin_config
        self.metric_config = metric_config

    def uuid(self) -> str:
        return generate_uuid("{};{}".format(self.audio_file_name, self.plugin_full_key))
