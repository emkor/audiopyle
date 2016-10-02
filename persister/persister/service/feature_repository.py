class FeatureRepository(object):
    def __init__(self, db_connector):
        """
        :type db_connector: persister.service.db_connector.DbConnector
        """
        self.db_connector = db_connector

    def store(self, audio_feature):
        """
        :type audio_feature: xtracter.model.feature.AudioFeature
        """
        raise NotImplementedError
