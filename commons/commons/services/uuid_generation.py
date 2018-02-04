from typing import Text, Any
from uuid import uuid5, UUID

SEED_TEXT = UUID(int=1248789574)


def generate_uuid(content: Any) -> Text:
    """
    :type content: object
    :rtype: str
    """
    return str(uuid5(SEED_TEXT, str(content)))


import numpy as np

mylist = [1.0, 2.0, 3.0, 2.0, 1.0, 0.0]
print(np.std(np.asanyarray(mylist)))