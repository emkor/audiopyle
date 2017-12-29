from typing import Text, List

from commons.abstractions.model import Model


class VampyPlugin(Model):
    def __init__(self, key: Text, categories: List[Text], outputs: List[Text], library_path: Text) -> None:
        """Represents VAMPy plugin for feature extraction"""
        self.key = key
        self.categories = categories
        self.outputs = outputs
        self.library_path = library_path

    @property
    def provider(self) -> Text:
        return self.key.split(":")[0]

    @property
    def name(self) -> Text:
        return self.key.split(":")[1]
