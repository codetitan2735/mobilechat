from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.mutable import MutableList

from db.base import Base


class ChatRoom(Base):

    name = Column(String)
    creator = Column(UUID)
    members = Column(MutableList.as_mutable(ARRAY(UUID)))
    chat_storage_id = Column(String, unique=True)
