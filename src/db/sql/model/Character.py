from sqlalchemy import Column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.types import VARCHAR, INTEGER, BINARY

from src.db.sql.model import Base


class Character(Base):
    __tablename__ = 'character'
    id = Column(INTEGER, primary_key=True)
    account_id = Column(INTEGER, ForeignKey('account.id'))
