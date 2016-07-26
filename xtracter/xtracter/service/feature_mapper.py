from xtracter.model.feature import RawFeature


class FeatureMapper(object):
    @staticmethod
    def from_dict(features_dict):
        if 'list' in features_dict:
            return FeatureMapper._handle_list_feature_type(features_dict)
        elif 'vector' in features_dict:
            return FeatureMapper._handle_vector_feature_type(features_dict)
        elif 'matrix' in features_dict:
            return FeatureMapper._handle_matrix_feature_type(features_dict)
        else:
            raise NotImplementedError("Did not suspected keys: {} from vamp features".format(features_dict.keys()))

    @staticmethod
    def _handle_list_feature_type(features_dict):
        output = []
        for feature_dict in features_dict.get('list'):
            timestamp = feature_dict.get("timestamp").to_float()
            values_list = feature_dict.get("values").tolist() if feature_dict.get("values") is not None else None
            output.append(RawFeature(timestamp=timestamp, value=values_list))
        return output

    @staticmethod
    def _handle_vector_feature_type(features_dict):
        step_seconds, values = features_dict.get('vector')
        output = []
        for index, value in enumerate(values):
            float_timestamp = step_seconds.to_float() * index
            list_values = value.tolist() if values is not None else None
            output.append(RawFeature(timestamp=float_timestamp, value=list_values))
        return output

    @staticmethod
    def _handle_matrix_feature_type(features_dict):
        step_seconds, values_matrix = features_dict.get('matrix')
        output = []
        for row, values in enumerate(values_matrix):
            float_timestamp = step_seconds.to_float() * row
            list_values = values.tolist() if values is not None else None
            output.append(RawFeature(timestamp=float_timestamp, value=list_values))
        return output
