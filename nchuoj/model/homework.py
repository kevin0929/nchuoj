from model.base import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)


__all__ = ["Homework", ]


class Homework(Base):
    __tablename__ = "homework"

    homeworkid = Column(Integer, primary_key=True)
    courseid = Column(Integer, ForeignKey("course.courseid"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    # auth
    is_show = Column(Boolean, default=True)

    # time information
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)


    def to_dict(self):
        return {
            "homeworkid": self.homeworkid,
            "courseid": self.courseid,
            "name": self.name,
            "description": self.description,
            "is_show": self.is_show,
            "start_date": self.start_date,
            "end_date": self.end_date
        }
