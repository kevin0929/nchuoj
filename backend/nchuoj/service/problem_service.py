import pandas as pd
import hashlib
from sqlalchemy.exc import SQLAlchemyError

from model.problem import Problem
from model.utils.db import *


class ProblemService:
    @staticmethod
    def delete_problem(
        problemid: int
    ):
        try:
            session = get_orm_session()

            problem = session.query(Problem).filter_by(problemid=problemid).first()

            if problem:
                session.delete(problem)
                session.commit()

        except SQLAlchemyError as err:
            session.rollback()
            print(f"Database error occured: {err}")
        finally:
            session.close()
