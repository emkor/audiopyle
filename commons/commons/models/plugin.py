from typing import Optional, Any, Dict

from commons.abstractions.model import Model


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
        return "{}:{}".format(self.vampy_key, self.output)


class VampyPluginParams(Model):
    def __init__(self, block_size: Optional[int], step_size: Optional[int], **params) -> None:
        self.step_size = step_size
        self.block_size = block_size
        self.params = params

    def to_vampy_dict(self) -> Dict[str, Any]:
        parameters = self.params or {}
        if self.step_size is not None:
            parameters.update({"step_size": self.step_size})
        if self.block_size is not None:
            parameters.update({"block_size": self.block_size})
        return parameters
