from commons.db.entity import FeatureMeta as FeatureMetaEntity
from commons.db.session import SessionProvider
from commons.models.result import FeatureMeta, DataStats, FeatureType
from commons.repository.abstract import DbRepository


class FeatureMetaRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, FeatureMetaEntity, map_feature_meta_entity_to_object,
                         map_feature_meta_object_to_entity)

    def get_by_task_id(self, task_id: str) -> FeatureMeta:
        return self._query_single_with_filters(task_id=task_id)

    def filter_by_type(self, feature_type: FeatureType):
        return self._query_multiple_with_filters(feature_type=feature_type.value)


def map_feature_meta_entity_to_object(feature_meta_entity: FeatureMetaEntity) -> FeatureMeta:
    data_stats = DataStats(minimum=feature_meta_entity.feature_minimum, maximum=feature_meta_entity.feature_maximum,
                           median=feature_meta_entity.feature_median, mean=feature_meta_entity.feature_mean,
                           standard_deviation=feature_meta_entity.feature_standard_deviation,
                           variance=feature_meta_entity.feature_variance)
    feature_type = FeatureType(feature_meta_entity.feature_type)
    return FeatureMeta(task_id=feature_meta_entity.task_id, plugin_output=feature_meta_entity.plugin_output,
                       feature_type=feature_type, feature_size=feature_meta_entity.feature_size_bytes,
                       data_shape=(feature_meta_entity.feature_shape_x, feature_meta_entity.feature_shape_y),
                       data_stats=data_stats)


def map_feature_meta_object_to_entity(feature_meta_object: FeatureMeta) -> FeatureMetaEntity:
    return FeatureMetaEntity(task_id=feature_meta_object.task_id, plugin_output=feature_meta_object.plugin_output,
                             feature_type=feature_meta_object.feature_type.value,
                             feature_shape_x=feature_meta_object.data_shape[0],
                             feature_shape_y=feature_meta_object.data_shape[1],
                             feature_size_bytes=feature_meta_object.feature_size,
                             feature_minimum=feature_meta_object.data_stats.minimum,
                             feature_maximum=feature_meta_object.data_stats.maximum,
                             feature_median=feature_meta_object.data_stats.median,
                             feature_mean=feature_meta_object.data_stats.mean,
                             feature_standard_deviation=feature_meta_object.data_stats.standard_deviation,
                             feature_variance=feature_meta_object.data_stats.variance)
