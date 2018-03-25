from typing import Optional

from commons.db.entity import FeatureMeta as FeatureMetaEntity
from commons.db.session import SessionProvider
from commons.models.result import FeatureMeta, DataStats, FeatureType
from commons.repository.abstract import DbRepository
from commons.utils.conversion import safe_cast


class FeatureMetaRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, FeatureMetaEntity)

    def filter_by_type(self, feature_type: FeatureType):
        return self._query_multiple(feature_type=feature_type.value)

    def get_id_by_model(self, model_object: FeatureMeta) -> Optional[str]:
        return safe_cast(self._get_id(id=model_object.task_id), str, None)

    def _map_to_object(self, entity: FeatureMetaEntity) -> FeatureMeta:
        data_stats = DataStats(minimum=entity.feature_minimum, maximum=entity.feature_maximum,
                               median=entity.feature_median, mean=entity.feature_mean,
                               standard_deviation=entity.feature_standard_deviation,
                               variance=entity.feature_variance)
        feature_type = FeatureType(entity.feature_type)
        return FeatureMeta(task_id=entity.id, feature_type=feature_type, feature_size=entity.feature_size_bytes,
                           data_shape=(entity.feature_shape_x, entity.feature_shape_y, entity.feature_shape_z),
                           data_stats=data_stats)

    def _map_to_entity(self, obj: FeatureMeta) -> FeatureMetaEntity:
        return FeatureMetaEntity(id=obj.task_id, feature_type=obj.feature_type.value,
                                 feature_shape_x=obj.data_shape[0],
                                 feature_shape_y=obj.data_shape[1],
                                 feature_shape_z=obj.data_shape[2],
                                 feature_size_bytes=obj.feature_size,
                                 feature_minimum=obj.data_stats.minimum,
                                 feature_maximum=obj.data_stats.maximum,
                                 feature_median=obj.data_stats.median,
                                 feature_mean=obj.data_stats.mean,
                                 feature_standard_deviation=obj.data_stats.standard_deviation,
                                 feature_variance=obj.data_stats.variance)
