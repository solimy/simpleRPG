from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


_engine = create_engine('sqlite:///simpleRPG.sql.db')

new_session = sessionmaker(bind=_engine)
