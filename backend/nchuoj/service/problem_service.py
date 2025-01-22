import pandas as pd
import hashlib
import io
import zipfile
from sqlalchemy.exc import SQLAlchemyError

from model.problem import Problem
from model.testcase import Testcase
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

    
    @staticmethod
    def add_problem(
        problem_info,
        testcases,
    ):
        try:
            session = get_orm_session()

            # add problem information into 'problem' table
            new_problem = Problem(**problem_info)
            session.add(new_problem)
            session.flush()     # to get probleid

            # 1. deal with testcase zip file (check, unzip, loop-deal)
            # 2. add testcase into 'testcase' table
            if testcases.filename.endswith(".zip"):
                zip_file_stream = io.BytesIO(testcases.read())

                with zipfile.ZipFile(zip_file_stream, 'r') as zf:
                    for filename in zf.namelist():
                        if not filename.endswith((".in", ".out")):
                            continue

                        # check a filename has in / out file at the same time
                        base_filename = filename.split(".")[0]
                        if not all(f"{base_filename}.{ext}" in zf.namelist() for ext in ["in", "out"]):
                            return {
                                "status": "error",
                                "msg": "One testcase should has in / out file at the same time!"
                            }
                        
                        # read content
                        with zf.open(filename) as file:
                            testcase_content = file.read()
                            print(testcase_content)

                        new_testcase = Testcase(
                            problemid=new_problem.problemid,
                            filename=filename,
                            content=testcase_content
                        )
                        session.add(new_testcase)
            
            session.commit()
            resp = {
                "status": "success",
                "msg": "New problem has been add!",
            }

            return resp

        except SQLAlchemyError as err:
            session.rollback()
            print(f"Database error occured: {err}")
        finally:
            session.close()
