from commons.abstraction import Model


class VampyPlugin(Model):
    def __init__(self, key, categories, outputs, library_path):
        """
        Represents VAMPy plugin for feature extraction
        :type key: str
        :type categories: list[str]
        :type outputs: list[str]
        :type library_path: str
        """
        self.key = key
        self.categories = categories
        self.outputs = outputs
        self.library_path = library_path

    @property
    def provider(self):
        """
        :rtype: str
        """
        return self.key.split(":")[0]

    @property
    def name(self):
        """
        :rtype: str
        """
        return self.key.split(":")[1]
