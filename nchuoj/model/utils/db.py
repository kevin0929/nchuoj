from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


def get_orm_session() -> Session():
    '''get sqlalchemy orm session
    '''

    url = "postgresql://nchuoj:nchuoj@database:5432/nchuoj_db"  # temporary show, it will store in variable env
    engine = create_engine(url)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session
