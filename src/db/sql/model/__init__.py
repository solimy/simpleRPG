from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .Account import Account
from .game.Entity import Entity
from .game.Position import Position
from .game.Image import Image
