from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import VARCHAR, INTEGER
from sqlalchemy import Column

from src.db.sql.model import Base


class Position(Base):
    __tablename__ = 'position'
    id = Column(ForeignKey('entity.id', ondelete='CASCADE'), primary_key=True)
    location = Column(VARCHAR(255))
    x = Column(INTEGER)
    y = Column(INTEGER)
    z = Column(INTEGER)
