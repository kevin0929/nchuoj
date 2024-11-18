from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from model import *


__all__ = ["get_orm_session", "get_user_course", ]


def get_orm_session() -> Session():
    '''get sqlalchemy orm session
    '''

    url = "postgresql://nchuoj:nchuoj@database:5432/nchuoj_db"  # temporary show, it will store in variable env
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def get_user_course(userid, courseid=None):
    session = get_orm_session()
    user = session.query(User).filter_by(userid=userid).first()
    course = session.query(Course).filter_by(courseid=courseid).first() if courseid else None

    if not user or (courseid and not course):
        abort(404)

    return user, course
