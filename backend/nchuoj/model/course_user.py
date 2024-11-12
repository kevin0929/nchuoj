from sqlalchemy import Column, Integer, ForeignKey
from model.base import Base


__all__ = ["CourseUser", ]


class CourseUser(Base):
    __tablename__ = "courseuser"

    cu_id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("users.userid"), nullable=False)
    courseid = Column(Integer, ForeignKey("course.courseid"), nullable=False)
