from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import VARCHAR

from src.db.sql.model import Base


class Character(Base):
    __tablename__ = 'character'
    id = Column(ForeignKey('entity.id'), primary_key=True)
    name = Column(VARCHAR(64), unique=True)
