from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from persister.entity.feature import Feature
from persister.service.db_engine import DbEngine


class Segment(DbEngine.get_base_entity_class()):
    __tablename__ = 'segment'

    id = Column(BigInteger, primary_key=True)

    offset = Column(BigInteger(), nullable=False)
    length = Column(BigInteger(), nullable=False)

    track_id = Column(BigInteger, ForeignKey('track.id'))
    track = relationship("Track", back_populates="segments")

    features = relationship("Feature", order_by=Feature.id, back_populates="segment")

    UniqueConstraint(track_id, offset, name='uix_segment')
