from sqlalchemy.types import BINARY, VARCHAR
from sqlalchemy import Column

from src.db.sql.model import Base


class Account(Base):
    __tablename__ = 'account'
    id = Column(BINARY(16), primary_key=True)
    username = Column(VARCHAR(64), primary_key=True)
    alias = Column(VARCHAR(64), unique=True)
    password = Column(BINARY(64))
    salt = Column(BINARY(16))
