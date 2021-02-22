from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import BINARY, BLOB

from src.db.sql.model import Base


class Image(Base):
    __tablename__ = 'image'
    id = Column(BINARY(16), primary_key=True)
    entity_id = Column(ForeignKey('entity.id'))
    blob = Column(BLOB(255))
