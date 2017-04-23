from uuid import uuid5, UUID

SEED_TEXT = UUID(int=1248789574)


def generate_uuid(content):
    """
    :type content: object
    :rtype: str
    """
    return str(uuid5(SEED_TEXT, str(content)))
