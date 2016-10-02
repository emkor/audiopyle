from sqlalchemy import BigInteger
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import SmallInteger
from sqlalchemy.orm import relationship
from persister.entity.segment import Segment
from persister.service.db_engine import DbEngine


class Track(DbEngine.get_base_entity_class()):
    __tablename__ = 'track'

    id = Column(BigInteger, primary_key=True)

    filename = Column(String(256))
    bit_depth = Column(SmallInteger())
    sample_rate = Column(Integer())
    frames_count = Column(BigInteger())
    channels_count = Column(SmallInteger())

    source_id = Column(Integer, ForeignKey('track_source.id'))
    source = relationship("TrackSource", back_populates="tracks")

    segments = relationship("Segment", order_by=Segment.id, back_populates="source")
