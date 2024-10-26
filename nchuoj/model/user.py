from model.base import Base

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Float
)
from sqlalchemy.ext.declarative import declarative_base

__all__ = ["users", ]


class User(Base):
    __tablename__ = "users"

    # basic information
    userid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    email = Column(String(128), nullable=False)
    full_name = Column(String(100))
    profile_picture = Column(String(200))   # path to the profile picture in server side
    message = Column(String(100))
    
    # auth
    role = Column(String(20), default="user")
    is_active = Column(Boolean, default=True)

    # statistic
    submission_count = Column(Integer, default=0)
    accepted_count = Column(Integer, default=0)
    rating = Column(Integer, default=1500)
    rank = Column(Integer, nullable=True)   # nullable to handle new user
