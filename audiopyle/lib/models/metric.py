from typing import Dict, Any

from audiopyle.lib.abstractions.model import Model
from audiopyle.lib.models.result import DataStats


class MetricDefinition(Model):
    def __init__(self, name: str, plugin_key: str, function: str, kwargs: dict) -> None:
        self.name = name
        self.plugin_key = plugin_key
        self.function = function
        self.kwargs = kwargs


class MetricValue(Model):
    def __init__(self, task_id: str, definition: MetricDefinition, stats: DataStats) -> None:
        self.task_id = task_id
        self.definition = definition
        self.stats = stats

    def to_serializable(self):
        base_serialized = super().to_serializable()
        base_serialized.update({"definition": self.definition.to_serializable(),
                                "stats": self.stats.to_serializable()})
        return base_serialized

    @classmethod
    def from_serializable(cls, serialized: Dict[str, Any]):
        stats_object = DataStats.from_serializable(serialized["stats"])
        definition_object = MetricDefinition.from_serializable(serialized["definition"])
        serialized.update({"stats": stats_object,
                           "definition": definition_object})
        return MetricValue(**serialized)
