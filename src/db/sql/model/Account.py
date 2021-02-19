from sqlalchemy.types import INTEGER, BINARY, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import Column

from src.db.sql.model import Base


class Account(Base):
    __tablename__ = 'account'
    id = Column(INTEGER, primary_key=True)
    username = Column(VARCHAR(255), unique=True)
    alias = Column(VARCHAR(255), unique=True)
    roles = Column(VARCHAR(255), nullable=True)
    password = Column(BINARY(64))
    salt = Column(BINARY(16))
