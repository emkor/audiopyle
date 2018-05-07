import json
from typing import Optional

from commons.models.metric import MetricDefinition as MetricDefObj
from commons.db.entity import MetricDefinition as MetricDefEnt
from commons.db.session import SessionProvider
from commons.models.plugin import full_key_to_params, params_to_full_key
from commons.repository.abstract import DbRepository
from commons.repository.vampy_plugin import VampyPluginRepository
from commons.utils.conversion import safe_cast


class MetricDefinitionRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider, plugin_repository: VampyPluginRepository) -> None:
        super().__init__(session_provider, MetricDefEnt)
        self.plugin_repository = plugin_repository

    def _map_to_entity(self, obj: MetricDefObj) -> MetricDefEnt:
        vendor, name, output = full_key_to_params(obj.plugin_key)
        vampy_plugin_id = self.plugin_repository.get_id_by_params(vendor, name, output)
        json_kwargs_repr = json.dumps(obj.kwargs)
        return MetricDefEnt(plugin_id=vampy_plugin_id, name=obj.name, function=obj.function, kwargs=json_kwargs_repr)

    def _map_to_object(self, entity: MetricDefEnt) -> MetricDefObj:
        plugin_entity = self.plugin_repository.get_by_id(entity.plugin_id)
        full_key = params_to_full_key(plugin_entity.vendor, plugin_entity.name, plugin_entity.output)
        model_kwargs = json.loads(entity.kwargs)
        return MetricDefObj(name=entity.name, plugin_key=full_key, function=entity.function, kwargs=model_kwargs)

    def get_id_by_model(self, model_object: MetricDefObj) -> Optional[int]:
        return safe_cast(self._get_id(id=model_object.name), int, None)
