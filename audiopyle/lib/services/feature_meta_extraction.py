from audiopyle.lib.models.feature import VampyFeatureAbstraction, VampyVariableStepFeature, VampyConstantStepFeature
from audiopyle.lib.models.result import FeatureMeta, FeatureType


def build_feature_meta(task_id: str, vampy_feature: VampyFeatureAbstraction) -> FeatureMeta:
    if isinstance(vampy_feature, VampyVariableStepFeature):
        return FeatureMeta(task_id=task_id, feature_type=FeatureType.VariableStepFeature,
                           feature_size=vampy_feature.size_bytes(),
                           data_shape=vampy_feature.value_shape())
    elif isinstance(vampy_feature, VampyConstantStepFeature):
        return FeatureMeta(task_id=task_id, feature_type=FeatureType.ConstantStepFeature,
                           feature_size=vampy_feature.size_bytes(),
                           data_shape=vampy_feature.value_shape())
    else:
        raise ValueError("Can not extract feature meta from: {}".format(vampy_feature))
