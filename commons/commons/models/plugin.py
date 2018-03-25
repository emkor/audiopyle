from typing import Optional, Dict, Any

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


class VampyPluginParamsDto(VampyPluginParams):
    def __init__(self, task_id: str, block_size: Optional[int], step_size: Optional[int], **params) -> None:
        super().__init__(block_size, step_size, **params)
        self.task_id = task_id

    @classmethod
    def from_serializable(cls, serialized: Dict[str, Any]) -> Any:
        task_id = serialized.pop("task_id")
        block_size = serialized.pop("block_size")
        step_size = serialized.pop("step_size")
        params = serialized.pop("params")
        return VampyPluginParamsDto(task_id=task_id, block_size=block_size, step_size=step_size, **params)
