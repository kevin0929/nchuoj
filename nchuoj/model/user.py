from model.base import Base

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base


class User(Base):
    __tablename__ = "users"

    userid = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    role = Column(String, nullable=False)

    __table_args__ = (UniqueConstraint("username"), UniqueConstraint("email"))
