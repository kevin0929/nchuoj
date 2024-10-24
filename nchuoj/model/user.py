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

    def get_userid(self):
        return self.userid


    def get_username(self):
        return self.username

    
    def set_username(self, username: str):
        self.username = username

    
    def get_password(self):
        return self.password

    
    def set_password(self, password: str):
        self.password = password


    def get_email(self):
        return self.email


    def set_email(self, email: str):
        self.email = email


    def get_full_name(self):
        return self.full_name


    def set_full_name(self, full_name: str):
        self.full_name = full_name


    def get_profile_picture(self):
        return self.profile_picture


    def set_profile_picture(self, profile_picture: str):
        self.profile_picture = profile_picture


    def get_message(self):
        return self.message


    def set_message(self, message: str):
        self.message = message


    def get_role(self):
        return self.role


    def set_role(self, role: str):
        '''role has three type'''

        valid_role = ["admin", "teacher", "TA", "user"]
        if role not in valid_role:
            pass

        self.role = role


    def get_is_active(self):
        return self.is_active


    def set_is_active(self, is_active: Boolean):
        self.is_active = is_active


    def get_submission_count(self):
        return self.submission_count


    def set_submission_count(self, submission_count: int):
        self.submission_count = submission_count


    def get_accepted_count(self):
        return self.accepted_count


    def set_accepted_count(self, accepted_count: int):
        self.accepted_count = accepted_count


    def get_rating(self):
        return self.rating


    def set_rating(self, rating: int):
        self.rating = rating


    def get_rank(self):
        return self.rank


    def set_rank(self, rank: int):
        self.rank = rank
