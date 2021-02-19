from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .Account import Account
from .Character import Character
