import pandas as pd
import hashlib
from sqlalchemy.exc import SQLAlchemyError

from model.user import User
from model.utils.db import *

class UserService:
    @staticmethod
    def hash_passwd(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()[:32]

    
    @staticmethod
    def import_user_by_csv(file):
        '''
            1. make dataframe from csv file by pandas library (read_csv)
            2. iterate dataframe to fetch user info
        '''
        try:
            session = get_orm_session()
            default_sticker = "img/logo_black.png"

            # read dataframe and do preprocess (remove the row all NaN)
            df = pd.read_csv(file)
            df = df.dropna(how="all")

            users_to_add = []
            for idx, row in df.iterrows():
                # skip already exist username (ex: student id)
                existing_user = session.query(User).filter_by(username=row["username"]).first()
                if existing_user:
                    print(f"Skipping row {idx}: duplicate username {row['username']}")
                    continue

                # necessary columns are username, password, email, role
                new_user = User(
                    username=row["username"],
                    password=UserService.hash_passwd(row["password"]),
                    email=row.get("email") if pd.notna(row.get("email")) else None,
                    role=row["role"],
                    full_name=row.get("full_name") if pd.notna(row.get("full_name")) else None,
                    profile_picture=default_sticker,
                    message=None,
                    submission_count=0,
                    accepted_count=0,
                    rating=1500,
                    rank=None,
                )
                users_to_add.append(new_user)

            if users_to_add:
                session.add_all(users_to_add)
                session.commit()
        
        except pd.errors.EmptyDataError:
            print("The provided CSV file is empty or invalid.")
        except SQLAlchemyError as err:
            session.rollback()
            print(f"Database error occured: {err}")
        finally:
            session.close()

    
    @staticmethod
    def add_user(
        username: str,
        password: str,
        email: str,
        role: str,
        full_name: str = None
    ):
        try:
            session = get_orm_session()
            default_sticker = "img/logo_black.png"

            # it is imposible that there has same username in this system
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                print(f"There has the same username : {username}")
                return

            new_user = User(
                username=username,
                password=UserService.hash_passwd(password),
                email=email,
                role=role,
                full_name=full_name,
                profile_picture=default_sticker,
                message=None,
                submission_count=0,
                accepted_count=0,
                rating=1500,
                rank=None,
            )

            session.add(new_user)
            session.commit()

        except SQLAlchemyError as err:
            session.rollback()
            print(f"Database error occured: {err}")
        finally:
            session.close()

    
    @staticmethod
    def edit(
        userid: int,
        username: str,
        password: str,
        email: str,
        role: str
    ):
        try:
            session = get_orm_session()

            # update user's new information
            user = session.query(User).filter_by(userid=userid).first()
            user.username = username
            if password:
                password = UserService.hash_passwd(password)
                user.password = password
            user.email = email
            user.role = role

            session.commit()

        except SQLAlchemyError as err:
            session.rollback()
            print(f"Database error occured: {err}")
        finally:
            session.close()

    
    @staticmethod
    def delete(
        userid: int
    ):
        try:
            session = get_orm_session()

            # delete user and it's information in other relation table
            user = session.query(User).filter_by(userid=userid).first()

            if user:
                session.delete(user)
                session.commit()

        except SQLAlchemyError as err:
            session.rollback()
            print(f"Database error occured: {err}")
        finally:
            session.close()
