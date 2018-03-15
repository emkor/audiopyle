from typing import List

from commons.db.entity import FeatureData
from commons.db.session import SessionProvider
from commons.models.compressed_feature import CompressedFeatureDTO, CompressionType
from commons.repository.abstract import DbRepository


class FeatureDataRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, FeatureData, map_feature_data_entity_to_object,
                         map_feature_data_object_to_entity)

    def get_by_task_id(self, task_id: str) -> CompressedFeatureDTO:
        return self._query_single_with_filters(task_id=task_id)

    def filter_by_compression(self, compression_type: CompressionType) -> List[CompressedFeatureDTO]:
        return self._query_multiple_with_filters(compression=compression_type.value)


def map_feature_data_entity_to_object(entity: FeatureData) -> CompressedFeatureDTO:
    return CompressedFeatureDTO(task_id=entity.task_id, compression=CompressionType(entity.compression),
                                data=entity.feature_data)


def map_feature_data_object_to_entity(feature_object: CompressedFeatureDTO) -> FeatureData:
    return FeatureData(task_id=feature_object.task_id, compression=feature_object.compression.value,
                       feature_data=feature_object.data)
