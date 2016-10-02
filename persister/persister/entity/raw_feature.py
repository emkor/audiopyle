from sqlalchemy import BigInteger
from sqlalchemy import Column, Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship

from persister.service.db_engine import DbEngine


class RawFeatureValue(DbEngine.get_base_entity_class()):
    __tablename__ = 'raw_feature_value'

    id = Column(BigInteger, primary_key=True)

    position = Column(Integer(), nullable=False)
    value = Column(Float(), nullable=False)

    raw_feature_id = Column(BigInteger, ForeignKey('raw_feature.id'))
    raw_feature = relationship("RawFeature", back_populates="raw_feature_values")


class RawFeature(DbEngine.get_base_entity_class()):
    __tablename__ = 'raw_feature'

    id = Column(BigInteger, primary_key=True)

    label = Column(String(100), nullable=True)
    timestamp = Column(Float(), nullable=False)

    feature_id = Column(BigInteger, ForeignKey('feature.id'))
    feature = relationship("Feature", back_populates="raw_features")

    raw_feature_values = relationship("RawFeatureValue", order_by=RawFeatureValue.id, back_populates="raw_feature")
