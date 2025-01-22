from model.base import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    LargeBinary
)


__all__ = ["Testcase", ]


class Testcase(Base):
    __tablename__ = "testcase"

    testcaseid = Column(Integer, primary_key=True, autoincrement=True)
    problemid = Column(Integer, ForeignKey("problem.problemid"), nullable=False)
    filename = Column(String, nullable=False)
    content = Column(LargeBinary, nullable=False)


    def to_dict(self):
        return {
            "testcaseid": self.testcaseid,
            "problemid": self.problemid,
            "filename": self.filename,
            "content": self.content
        }
