from typing import List

from commons.db.entity import FeatureData
from commons.db.session import SessionProvider
from commons.models.compressed_feature import CompressedFeatureDTO, CompressionType
from commons.repository.abstract import DbRepository


class FeatureDataRepository(DbRepository):
    def __init__(self, session_provider: SessionProvider) -> None:
        super().__init__(session_provider, FeatureData)

    def get_by_task_id(self, task_id: str) -> CompressedFeatureDTO:
        return self._query_single_with_filters(task_id=task_id)

    def filter_by_compression(self, compression_type: CompressionType) -> List[CompressedFeatureDTO]:
        return self._query_multiple_with_filters(compression=compression_type.value)

    def _get_id_by_model(self, model_object: CompressedFeatureDTO) -> int:
        return self._get_id(task_id=model_object.task_id)

    def _map_to_object(self, entity: FeatureData) -> CompressedFeatureDTO:
        return CompressedFeatureDTO(task_id=entity.task_id, compression=CompressionType(entity.compression),
                                    data=entity.feature_data)

    def _map_to_entity(self, obj: CompressedFeatureDTO) -> FeatureData:
        return FeatureData(task_id=obj.task_id, compression=obj.compression.value, feature_data=obj.data)
