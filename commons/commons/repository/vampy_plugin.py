from typing import List

from commons.db.entity import VampyPlugin as VampyPluginEntity
from commons.db.session import SessionProvider
from commons.models.plugin import VampyPlugin
from commons.repository.abstract import DbRepository


class VampyPluginRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, VampyPluginEntity)

    def get_id_by_params(self, vendor: str, name: str, output: str) -> int:
        return super()._get_id(vendor=vendor, name=name, output=output)

    def filter_by_vendor(self, vendor: str) -> List[VampyPlugin]:
        return self._query_multiple(vendor=vendor)

    def get_id_by_model(self, model_object: VampyPlugin) -> int:
        return self.get_id_by_params(vendor=model_object.vendor, name=model_object.name, output=model_object.output)

    def _map_to_object(self, entity: VampyPluginEntity) -> VampyPlugin:
        return VampyPlugin(vendor=entity.vendor, name=entity.name, output=entity.output,
                           library_file_name=entity.library_file_name)

    def _map_to_entity(self, obj: VampyPlugin) -> VampyPluginEntity:
        return VampyPluginEntity(vendor=obj.vendor, name=obj.name, output=obj.output,
                                 library_file_name=obj.library_file_name)
