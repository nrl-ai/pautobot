import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from pautobot.database import Base, engine


class BotContext(Base):
    __tablename__ = "contexts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    documents = relationship("Document", back_populates="bot_context")
    chat_chunks = relationship("ChatChunk", back_populates="bot_context")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    storage_name = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    bot_context_id = Column(Integer, ForeignKey("contexts.id"))
    bot_context = relationship("BotContext", back_populates="documents")


class ChatChunk(Base):
    __tablename__ = "chat_chunks"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    text = Column(String)
    bot_context_id = Column(Integer, ForeignKey("contexts.id"))
    bot_context = relationship("BotContext", back_populates="chat_chunks")


Base.metadata.create_all(engine)
