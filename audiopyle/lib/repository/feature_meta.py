from typing import Optional

from audiopyle.lib.db.entity import FeatureMeta as FeatureMetaEntity
from audiopyle.lib.db.session import SessionProvider
from audiopyle.lib.models.result import FeatureMeta, FeatureType
from audiopyle.lib.repository.abstract import DbRepository
from audiopyle.lib.utils.conversion import safe_cast


class FeatureMetaRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, FeatureMetaEntity)

    def filter_by_type(self, feature_type: FeatureType):
        return self._query_multiple(feature_type=feature_type.value)

    def get_id_by_model(self, model_object: FeatureMeta) -> Optional[str]:
        return safe_cast(self._get_id(id=model_object.task_id), str, None)

    def _map_to_object(self, entity: FeatureMetaEntity) -> FeatureMeta:
        feature_type = FeatureType(entity.feature_type)
        return FeatureMeta(task_id=entity.id, feature_type=feature_type, feature_size=entity.feature_size_bytes,
                           data_shape=(entity.feature_shape_x, entity.feature_shape_y, entity.feature_shape_z))

    def _map_to_entity(self, obj: FeatureMeta) -> FeatureMetaEntity:
        return FeatureMetaEntity(id=obj.task_id, feature_type=obj.feature_type.value,
                                 feature_shape_x=obj.data_shape[0],
                                 feature_shape_y=obj.data_shape[1],
                                 feature_shape_z=obj.data_shape[2],
                                 feature_size_bytes=obj.feature_size)
