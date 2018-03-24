from commons.abstractions.model import Model


class VampyPlugin(Model):
    def __init__(self, vendor: str, name: str, output: str, library_file_name: str) -> None:
        """Represents VAMPy plugin for feature extraction"""
        self.vendor = vendor
        self.name = name
        self.output = output
        self.library_file_name = library_file_name

    @property
    def vampy_key(self) -> str:
        return "{}:{}".format(self.vendor, self.name)

    @property
    def full_key(self) -> str:
        return "{}:{}".format(self.vampy_key, self.output)
