from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import BINARY
from sqlalchemy import Column

from src.db.sql.model import Base


class Entity(Base):
    __tablename__ = 'entity'
    id = Column(BINARY(16), primary_key=True)
    account_id = Column(ForeignKey('account.id'), nullable=True)
