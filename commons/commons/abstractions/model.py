from copy import copy


class Model(object):
    @classmethod
    def deserialize(cls, serialized):
        return cls(**serialized)

    def serialize(self):
        return copy(self.__dict__)

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
