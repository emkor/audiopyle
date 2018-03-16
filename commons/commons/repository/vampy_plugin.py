from typing import List

from commons.db.entity import VampyPlugin as VampyPluginEntity
from commons.db.session import SessionProvider
from commons.models.plugin import VampyPlugin
from commons.repository.abstract import DbRepository
from commons.services.plugin_providing import VampyPluginProvider


class VampyPluginRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider, plugin_provider: VampyPluginProvider) -> None:
        super().__init__(session_provider, VampyPluginEntity)
        self.plugin_provider = plugin_provider

    def get_id_by_vendor_and_name(self, vendor: str, name: str) -> int:
        return super()._get_id(vendor=vendor, name=name)

    def filter_by_vendor(self, vendor: str) -> List[VampyPlugin]:
        return self._query_multiple_with_filters(vendor=vendor)

    def get_id_by_model(self, model_object: VampyPlugin) -> int:
        return self.get_id_by_vendor_and_name(vendor=model_object.provider, name=model_object.name)

    def _map_to_object(self, entity: VampyPluginEntity) -> VampyPlugin:
        plugin_key = "{}:{}".format(entity.vendor, entity.name)
        return self.plugin_provider.build_plugin_from_key(plugin_key)

    def _map_to_entity(self, obj: VampyPlugin) -> VampyPluginEntity:
        return VampyPluginEntity(vendor=obj.provider, name=obj.name)
