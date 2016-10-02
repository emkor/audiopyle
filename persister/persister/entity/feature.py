from sqlalchemy import BigInteger
from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from persister.entity.raw_feature import RawFeature
from persister.service.db_engine import DbEngine


class Feature(DbEngine.get_base_entity_class()):
    __tablename__ = 'feature'

    id = Column(BigInteger, primary_key=True)

    plugin_id = Column(Integer, ForeignKey('plugin.id'))
    plugin = relationship("Plugin", back_populates="features")

    segment_id = Column(BigInteger, ForeignKey('segment.id'))
    segment = relationship("Segment", back_populates="features")

    raw_features = relationship("RawFeature", order_by=RawFeature.id, back_populates="feature")
