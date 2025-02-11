from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from model.course_user import CourseUser
from model.user import User
from model.utils.db import *


class CourseUserService:
    @staticmethod
    def add_course_user(
        userid: int,
        courseid: int
    ):
        '''
        '''
        try:
            session = get_orm_session()

            new_course_user = CourseUser(
                userid=userid,
                courseid=courseid
            )

            if new_course_user:
                session.add(new_course_user)
                session.commit()

        except SQLAlchemyError as err: 
            session.rollback()
            print(f"Database error occured: {err}")
        finally:
            session.close()


    @staticmethod
    def delete_course_user(cu_id: int) -> int:
        '''will return courseid
        '''
        try:
            session = get_orm_session()

            course_user = session.query(CourseUser).filter_by(cu_id=cu_id).first()
            course_user_info = course_user.to_dict()
            if course_user:
                session.delete(course_user)
                session.commit()

                return course_user_info["courseid"]
        
        except SQLAlchemyError as err:
            session.rollback()
            print(f"Database error occured: {err}")
        finally:
            session.close()
