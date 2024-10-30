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
    is_activate = Column(Boolean, default=True)

    # statistic
    submission_count = Column(Integer, default=0)
    accepted_count = Column(Integer, default=0)
    rating = Column(Integer, default=1500)
    rank = Column(Integer, nullable=True)   # nullable to handle new user


    def to_dict(self):
        return {
            "userid": self.userid,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "full_name": self.full_name,
            "profile_picture": self.profile_picture,
            "message": self.message,
            "role": self.role,
            "is_activate": self.is_activate,
            "submission_count": self.submission_count,
            "accepted_count": self.accepted_count,
            "rating": self.rating,
            "rank": self.rank,
        }
