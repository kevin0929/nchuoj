from model.base import Base

from sqlalchemy import (
    Column,
    Integer,
    Enum,
    ForeignKey,
)
from sqlalchemy.orm import relationship


__all__ = ["UserProblemScore", ]


class UserProblemScore(Base):
    __tablename__ = "user_problem_score"

    ups_id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("users.userid"), nullable=False)
    problemid = Column(Integer, ForeignKey("problem.problemid"), nullable=False)
    score = Column(Integer, nullable=False)
    status = Column(Enum("AC", "WA", "TLE", "CE", "OTHER", name="submission_status"), nullable=False)


    def to_dict(self):
        return {
            "ups_id": self.ups_id,
            "userid": self.userid,
            "problemid": self.problemid,
            "score": self.score,
            "status": self.status
        }
