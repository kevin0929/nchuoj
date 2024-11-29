from model.base import Base

from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Boolean,
    DateTime,
    UniqueConstraint,
    ForeignKey,
)
from sqlalchemy.orm import relationship


__all__ = ["Course", ]


class Course(Base):
    __tablename__ = "course"

    courseid = Column(Integer, primary_key=True, autoincrement=True)
    coursename = Column(String, nullable=False)
    teacher = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # auth
    is_activate = Column(Boolean, nullable=False, server_default="true")
    is_public = Column(Boolean, nullable=False, server_default="false")

    # time information
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)

    # relationship with courseuser
    course_users = relationship("CourseUser", cascade="all, delete-orphan", backref="course")


    def to_dict(self):
        return {
            "courseid": self.courseid,
            "coursename": self.coursename,
            "teacher": self.teacher,
            "description": self.description,
            "is_activate": self.is_activate,
            "is_public": self.is_public,
            "start_date": self.start_date,
            "end_date": self.end_date
        }
