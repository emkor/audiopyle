from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from persister.entity.feature import Feature
from persister.service.db_engine import DbEngine


class Plugin(DbEngine.get_base_entity_class()):
    __tablename__ = 'plugin'

    id = Column(Integer, primary_key=True)
    plugin_key = Column(String(100))
    output = Column(String(50))
    features = relationship("Feature", order_by=Feature.id, back_populates="plugin")
