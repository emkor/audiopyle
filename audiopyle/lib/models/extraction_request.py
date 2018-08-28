from typing import Any, Dict, Optional, Type

from audiopyle.lib.abstractions.model import Model
from audiopyle.lib.services.uuid_generation import generate_uuid


class ExtractionRequest(Model):
    def __init__(self, audio_file_name: str, plugin_full_key: str,
                 plugin_config: Optional[Dict[str, Any]] = None,
                 metric_config: Optional[Dict[str, Any]] = None) -> None:
        self.audio_file_name = audio_file_name
        self.plugin_full_key = plugin_full_key
        self.uuid = generate_uuid("{};{}".format(self.audio_file_name, self.plugin_full_key))
        self.plugin_config = plugin_config
        self.metric_config = metric_config

    @classmethod
    def from_serializable(cls: Type, serialized: Dict[str, Any]) -> Any:
        original_uuid = serialized.pop("uuid", None)
        super_deserialized = super().from_serializable(serialized)
        if original_uuid != super_deserialized.uuid and original_uuid is not None:
            raise ValueError("Deserialized and generated UUIDs do not match: {}".format(super_deserialized))
        return super_deserialized

    def to_serializable(self) -> Dict[str, Any]:
        super_serialized = super().to_serializable()
        super_serialized.pop("uuid")
        return super_serialized
