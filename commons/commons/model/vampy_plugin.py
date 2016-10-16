SEPARATOR = ":"


class VampyPlugin(object):
    def __init__(self, key, outputs, category):
        self.key = key
        self.category = category
        self.outputs = outputs

    def get_provider(self):
        return self.key.split(SEPARATOR)[0]

    def get_name(self):
        return self.key.split(SEPARATOR)[1]

    def __str__(self):
        return 'Analyzer key: {} category: {} outputs: {}'.format(self.key, self.category, self.outputs)
