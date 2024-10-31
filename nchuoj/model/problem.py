from model.base import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
)


__all__ = ["Problem", ]


class Problem(Base):
    __tablename__ = "problem"

    problemid = Column(Integer, primary_key=True)
    homeworkid = Column(Integer, ForeignKey("homework.homeworkid"), nullable=False)
    score = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    tag = Column(String, nullable=True)

    # auth
    is_show = Column(Boolean, default=True)


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
