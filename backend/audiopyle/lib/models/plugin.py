from typing import Optional, Dict, Any, Tuple

from audiopyle.lib.abstractions.model import Model


def full_key_to_params(vampy_full_key: str) -> Tuple[str, str, str]:
    key_parts = vampy_full_key.split(":")
    if len(key_parts) != 3:
        raise ValueError("Can not parse {} as Vampy plugin key!".format(vampy_full_key))
    return key_parts[0], key_parts[1], key_parts[2]


def params_to_full_key(vendor: str, name: str, output: str) -> str:
    return "{}:{}:{}".format(vendor, name, output)


class VampyPlugin(Model):
    def __init__(self, vendor: str, name: str, output: str, library_file_name: str) -> None:
        """Represents VAMPy plugin for feature extraction"""
        self.vendor = vendor
        self.name = name
        self.output = output
        self.library_file_name = library_file_name

    @property
    def vampy_key(self) -> str:
        return "{}:{}".format(self.vendor, self.name)

    @property
    def full_key(self) -> str:
        return params_to_full_key(self.vendor, self.name, self.output)


class VampyPluginParams(Model):
    def __init__(self, block_size: Optional[int], step_size: Optional[int], **params) -> None:
        self.step_size = step_size
        self.block_size = block_size
        self.params = params

    @classmethod
    def from_serializable(cls, serialized: Dict[str, Any]) -> Any:
        block_size = serialized.pop("block_size")
        step_size = serialized.pop("step_size")
        params = serialized.pop("params")
        return VampyPluginParams(block_size=block_size, step_size=step_size, **params)

    def extraction_params(self):
        parameters = self.params or {}
        if self.step_size is not None:
            parameters.update({"step_size": self.step_size})
        if self.block_size is not None:
            parameters.update({"block_size": self.block_size})
        return parameters
