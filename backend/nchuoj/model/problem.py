from model.base import Base

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship


__all__ = ["Problem", ]


class Problem(Base):
    __tablename__ = "problem"

    problemid = Column(Integer, primary_key=True, autoincrement=True)
    homeworkid = Column(Integer, ForeignKey("homework.homeworkid"), nullable=False)
    score = Column(Integer, nullable=False)
    memory_limit = Column(Float, nullable=False, server_default="256.0")   # kb
    runtime_limit = Column(Float, nullable=False, server_default="1.0")    # s
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    input_format = Column(String, nullable=False)
    output_format = Column(String, nullable=False)
    tag = Column(String, nullable=True)

    # sample
    sample_input_1 = Column(String, nullable=True)
    sample_output_1 = Column(String, nullable=True)
    sample_input_2 = Column(String, nullable=True)
    sample_output_2 = Column(String, nullable=True)
    sample_input_3 = Column(String, nullable=True)
    sample_output_3 = Column(String, nullable=True)

    # auth
    is_show = Column(Boolean, nullable=False, server_default="true")

    # relation
    submissions = relationship("Submission", cascade="all, delete-orphan", backref="problem")
    testcases = relationship("Testcase", cascade="all, delete-orphan", backref="problem")


    def to_dict(self):
        return {
            "problemid": self.problemid,
            "homeworkid": self.homeworkid,
            "score": self.score,
            "memory_limit": self.memory_limit,
            "runtime_limit": self.runtime_limit,
            "name": self.name,
            "description": self.description,
            "input_format": self.input_format,
            "output_format": self.output_format,
            "tag": self.tag,
            "sample_input_1": self.sample_input_1,
            "sample_output_1": self.sample_output_1,
            "sample_input_2": self.sample_input_2,
            "sample_output_2": self.sample_output_2,
            "sample_input_3": self.sample_input_3,
            "sample_output_3": self.sample_output_3,
            "is_show": self.is_show
        }
