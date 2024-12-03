from sqlalchemy import Column, String

from db.base import Base


class User(Base):

    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
