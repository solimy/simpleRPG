from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Binary, String

from src.db.sql import _engine


_Base = declarative_base()


class User(_Base):
    __tablename__ = 'users'
    alias = Column(String, unique=True)
    username = Column(String, primary_key=True)
    password = Column(Binary)
    salt = Column(Binary)
    roles = Column(String, nullable=True)


_Base.metadata.create_all(_engine)
