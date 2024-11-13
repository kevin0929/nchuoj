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
    input_data = Column(LargeBinary, nullable=False)
    output_data = Column(LargeBinary, nullable=False)


    def to_dict(self):
        return {
            "testcaseid": self.testcaseid,
            "problemid": self.problemid,
            "input_data": self.input_data,
            "output_data": self.output_data
        }
