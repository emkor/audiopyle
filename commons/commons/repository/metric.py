import json
from typing import Optional

from commons.models.metric import MetricDefinition as MetricDefObj, MetricValue
from commons.db.entity import MetricDefinition as MetricDefEnt, VampyPlugin, Metric
from commons.db.session import SessionProvider
from commons.models.plugin import full_key_to_params, params_to_full_key
from commons.models.result import DataStats
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
        plugin_entity = self.plugin_repository.get_by_id(entity.plugin_id)  # type: Optional[VampyPlugin]
        if plugin_entity:
            full_key = params_to_full_key(plugin_entity.vendor, plugin_entity.name, plugin_entity.output)
            model_kwargs = json.loads(entity.kwargs)
            return MetricDefObj(name=entity.name, plugin_key=full_key, function=entity.function, kwargs=model_kwargs)
        raise ValueError(
            "Could not find plugin with ID of {} when resolving metric definition named {}".format(entity.plugin_id,
                                                                                                   entity.name))

    def get_id_by_model(self, model_object: MetricDefObj) -> Optional[int]:
        return safe_cast(self._get_id(id=model_object.name), int, None)


class MetricValueRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider, definition_repository: MetricDefinitionRepository) -> None:
        super().__init__(session_provider, Metric)
        self.definition_repository = definition_repository

    def _map_to_entity(self, obj: MetricValue) -> Metric:
        definition_id = self.definition_repository.get_id_by_model(obj.definition)
        return Metric(task_id=obj.task_id, definition_id=definition_id,
                      minimum=obj.stats.minimum, maximum=obj.stats.maximum,
                      median=obj.stats.median, mean=obj.stats.mean,
                      standard_deviation=obj.stats.standard_deviation, variance=obj.stats.variance)

    def _map_to_object(self, entity: Metric) -> MetricValue:
        definition_object = self.definition_repository.get_by_id(entity.definition_id)
        if not definition_object:
            raise ValueError("Could not find metric definition with id {} for metric {}".format(entity.definition_id,
                                                                                                entity.task_id))
        data_stats = DataStats(minimum=entity.minimum, maximum=entity.maximum,
                               median=entity.median, mean=entity.mean,
                               standard_deviation=entity.standard_deviation, variance=entity.variance)
        return MetricValue(task_id=entity.task_id, definition=definition_object, stats=data_stats)

    def get_id_by_model(self, model_object: MetricValue) -> Optional[int]:
        definition_id = self.definition_repository.get_id_by_model(model_object.definition)
        return safe_cast(self._get_id(definition_id=definition_id, task_id=model_object.task_id), int, None)
