from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from model.course import Course
from model.utils.db import *


class CourseService:
    @staticmethod
    def add_course(
        coursename: str,
        teacher: str,
        start_date: str,
        end_date: str,
        is_activate: bool
    ):
        '''
        '''
        try:
            session = get_orm_session()

            # format `start_date` and `end_date`
            start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M")
            end_date = datetime.strptime(end_date, "%Y-%m-%dT%H:%M")

            new_course = Course(
                coursename=coursename,
                teacher=teacher,
                start_date=start_date,
                end_date=end_date,
                is_activate=is_activate.lower() == "true",
                is_public=True,
            )

            if new_course:
                session.add(new_course)
                session.commit()

        except SQLAlchemyError as err: 
            session.rollback()
            print(f"Database error occured: {err}")
        finally:
            session.close()


    @staticmethod
    def delete_course(courseid: int):
        '''
        '''
        try:
            session = get_orm_session()

            course = session.query(Course).filter_by(courseid=courseid).first()

            if course:
                session.delete(course)
                session.commit()
        
        except SQLAlchemyError as err: 
            session.rollback()
            print(f"Database error occured: {err}")
        finally:
            session.close()
