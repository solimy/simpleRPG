from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import BINARY, VARCHAR
import asyncio

from src.db.sql import get_engine


_Base = declarative_base()


class User(_Base):
    __tablename__ = 'users'
    alias = Column(VARCHAR(255), unique=True)
    username = Column(VARCHAR(255), primary_key=True)
    roles = Column(VARCHAR(255), nullable=True)
    password = Column(BINARY(64))
    salt = Column(BINARY(16))
