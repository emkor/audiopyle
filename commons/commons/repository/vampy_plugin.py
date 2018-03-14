from typing import List

from commons.db.entity import VampyPlugin as VampyPluginEntity
from commons.db.session import SessionProvider
from commons.models.plugin import VampyPlugin
from commons.repository.abstract import DbRepository
from commons.services.plugin_providing import build_plugin_from_key


class VampyPluginRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, VampyPluginEntity, map_plugin_entity_to_object, map_plugin_object_to_entity)

    def get_id_by_vendor_and_name(self, vendor: str, name: str) -> int:
        return super()._get_id(vendor=vendor, name=name)

    def filter_by_vendor(self, vendor: str) -> List[VampyPlugin]:
        return self._query_multiple_with_filters(vendor=vendor)


def map_plugin_entity_to_object(plugin_entity: VampyPluginEntity) -> VampyPlugin:
    plugin_key = "{}:{}".format(plugin_entity.vendor, plugin_entity.name)
    return build_plugin_from_key(plugin_key)


def map_plugin_object_to_entity(plugin_object: VampyPlugin) -> VampyPluginEntity:
    return VampyPluginEntity(vendor=plugin_object.provider, name=plugin_object.name)
