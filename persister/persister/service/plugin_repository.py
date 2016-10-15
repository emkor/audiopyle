from persister.entity.plugin import Plugin


class PluginRepository(object):
    def __init__(self, db_connector):
        """
        :type db_connector: persister.service.db_connector.DbConnector
        """
        self.db_connector = db_connector

    def store(self, plugin_key, plugin_output):
        """
        :type plugin_key: str
        :type plugin_output: str
        :rtype: persister.entity.plugin.Plugin
        """
        plugin_entity = self.retrieve(plugin_key, plugin_output) or Plugin(plugin_key=plugin_key, output=plugin_output)
        session = self.db_connector.get_db_session()
        session.add(plugin_entity)
        return plugin_entity

    def retrieve(self, plugin_key, plugin_output):
        """
        :type plugin_key: str
        :type plugin_output: str
        :rtype: persister.entity.plugin.Plugin
        """
        session = self.db_connector.get_db_session()
        try:
            return session.query(Plugin) \
                .filter(Plugin.plugin_key == plugin_key) \
                .filter(Plugin.output == plugin_output) \
                .one_or_none()
        except Exception as e:
            print("Could not check if given plugin: {} with output: {} exists in DB. Details: {}".format(plugin_key,
                                                                                                         plugin_output,
                                                                                                         e))
