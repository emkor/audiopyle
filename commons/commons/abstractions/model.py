import json


class Model(object):
    def __str__(self):
        """
        :rtype: str
        """
        return "{}: {}".format(self.__class__.__name__, self.__dict__)

    def __repr__(self):
        """
        :rtype: str
        """
        return self.__str__()

    def __eq__(self, other):
        """
        :type other: commons.model.Model
        :rtype: bool
        """
        return self.__dict__ == other.__dict__

    def __hash__(self):
        """
        :rtype: str
        """
        return hash(self.__dict__)

    def serialize(self):
        """
        :rtype: str
        """
        return json.dumps(self.__dict__)
