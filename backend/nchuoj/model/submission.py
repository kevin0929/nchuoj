from model.base import Base

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    DateTime,
    ForeignKey,
)


__all__ = ["Submission", ]


class Submission(Base):
    __tablename__ = "submission"

    submissionid = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey("users.userid"), nullable=False)
    problemid = Column(Integer, ForeignKey("problem.problemid"), nullable=False)
    runtime = Column(Float, nullable=False)
    memory = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    language = Column(String, nullable=False)
    status = Column(String, nullable=False)

    # time information
    submit_time = Column(DateTime, nullable=True)


    def to_dict(self):
        return {
            "submissionid": self.submissionid,
            "userid": self.userid,
            "problemid": self.problemid,
            "runtime": self.runtime,
            "memory": self.memory,
            "score": self.score,
            "language": self.language,
            "status": self.status,
            "submit_time": self.submit_time
        }
