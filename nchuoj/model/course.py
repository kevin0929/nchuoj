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

__all__ = ["Course", ]


class Course(Base):
    __tablename__ = "course"

    courseid = Column(Integer, primary_key=True)
    coursename = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
