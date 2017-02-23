from commons.abstraction import Model


class VampyPlugin(Model):
    def __init__(self, provider, name, categories, outputs, library_path):
        """
        Represents VAMPy plugin for feature extraction
        :type provider: str
        :type name: str
        :type categories: list[str]
        :type outputs: list[str]
        :type library_path: str
        """
        self.provider = provider
        self.name = name
        self.categories = categories
        self.outputs = outputs
        self.library_path = library_path

    @property
    def key(self):
        """
        Returns standard VAMP plugin key
        :rtype: str
        """
        return "{}:{}".format(self.provider, self.name)
