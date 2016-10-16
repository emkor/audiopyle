from persister.entity.plugin import Plugin
from persister.entity.raw_feature import RawFeature, RawFeatureValue
from persister.entity.segment import Segment
from persister.entity.track import Track


class FeatureRepository(object):
    def __init__(self, db_connector):
        """
        :type db_connector: persister.service.db_connector.DbConnector
        """
        self.db_connector = db_connector

    def store(self, audio_feature):
        """
        :type audio_feature: commons.model.feature.AudioFeature
        """
        session = self.db_connector.get_db_session()
        plugin_entity = self._retrieve_plugin_entity_if_exists(session, audio_feature.plugin_key,
                                                               audio_feature.plugin_output)
        plugin_entity = plugin_entity or Plugin(plugin_key=audio_feature.plugin_key,
                                                output=audio_feature.plugin_output)
        session.add(plugin_entity)

        track_entity = Track(filename=audio_feature.audio_meta.filename, bit_depth=audio_feature.audio_meta.bit_depth,
                             sample_rate=audio_feature.audio_meta.sample_rate,
                             frames_count=audio_feature.audio_meta.frames_count,
                             channels_count=audio_feature.audio_meta.channels_count)
        segment_entity = Segment(offset=audio_feature.segment_meta.offset, length=audio_feature.segment_meta.length)
        raw_feature_entities = []
        for raw_feature in audio_feature.raw_features:
            values = raw_feature.value
            value_entities = []
            if not isinstance(values, list):
                values = [values]
            for index, value in enumerate(values):
                value_entities.append(RawFeatureValue(position=index, value=value))
            raw_feature_entities.append(RawFeature(label=raw_feature.label if raw_feature.label else None,
                                                   timestamp=raw_feature.timestamp, raw_feature_values=value_entities))

        raise NotImplementedError

    def _retrieve_plugin_entity_if_exists(self, session, plugin_key, plugin_output):
        try:
            return session.query(Plugin) \
                .filter(Plugin.plugin_key == plugin_key) \
                .filter(Plugin.output == plugin_output) \
                .one_or_none()
        except Exception as e:
            print("Could not check if given plugin: {} with output: {} exists in DB. Details: {}".format(plugin_key,
                                                                                                         plugin_output,
                                                                                                         e))
