from typing import List, Optional

import json

from audiopyle.commons.db.entity import VampyPlugin as VampyPluginEntity, PluginConfig
from audiopyle.commons.db.session import SessionProvider
from audiopyle.commons.models.plugin import VampyPlugin, VampyPluginParams
from audiopyle.commons.repository.abstract import DbRepository
from audiopyle.commons.utils.conversion import safe_cast

PLUGIN_CONFIG_DEFAULT = 0


class VampyPluginRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, VampyPluginEntity)

    def get_id_by_params(self, vendor: str, name: str, output: str) -> Optional[int]:
        return safe_cast(super()._get_id(vendor=vendor, name=name, output=output), int, None)

    def filter_by_vendor(self, vendor: str) -> List[VampyPlugin]:
        return self._query_multiple(vendor=vendor)

    def get_id_by_model(self, model_object: VampyPlugin) -> Optional[int]:
        return safe_cast(
            self.get_id_by_params(vendor=model_object.vendor, name=model_object.name, output=model_object.output), int,
            None)

    def _map_to_object(self, entity: VampyPluginEntity) -> VampyPlugin:
        return VampyPlugin(vendor=entity.vendor, name=entity.name, output=entity.output,
                           library_file_name=entity.library_file_name)

    def _map_to_entity(self, obj: VampyPlugin) -> VampyPluginEntity:
        return VampyPluginEntity(vendor=obj.vendor, name=obj.name, output=obj.output,
                                 library_file_name=obj.library_file_name)


class PluginConfigRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, PluginConfig)

    def _map_to_entity(self, obj: VampyPluginParams) -> PluginConfig:
        additional_params = json.dumps(obj.params, sort_keys=True)
        return PluginConfig(block_size=safe_cast(obj.block_size, int, PLUGIN_CONFIG_DEFAULT),
                            step_size=safe_cast(obj.step_size, int, PLUGIN_CONFIG_DEFAULT),
                            additional_params=additional_params)

    def _map_to_object(self, entity: PluginConfig) -> VampyPluginParams:
        block_size = entity.block_size if entity.block_size != PLUGIN_CONFIG_DEFAULT else None
        step_size = entity.step_size if entity.step_size != PLUGIN_CONFIG_DEFAULT else None
        return VampyPluginParams(block_size=block_size, step_size=step_size,
                                 **json.loads(entity.additional_params))

    def get_id_by_model(self, model_object: VampyPluginParams) -> Optional[int]:
        additional_params = json.dumps(model_object.params, sort_keys=True)
        return safe_cast(self._get_id(block_size=safe_cast(model_object.block_size, int, PLUGIN_CONFIG_DEFAULT),
                                      step_size=safe_cast(model_object.step_size, int, PLUGIN_CONFIG_DEFAULT),
                                      additional_params=additional_params),
                         int, None)
