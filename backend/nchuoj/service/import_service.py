import pandas as pd
import hashlib
from sqlalchemy.exc import SQLAlchemyError

from model.user import User
from model.utils.db import *

class ImportService:
    def __init__(self):
        self.session = get_orm_session()
        self.default_sticker = "img/logo_black.png"

    
    def hash_passwd(self, password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()[:32]

    
    def import_user_by_csv(self, file):
        '''
            1. make dataframe from csv file by pandas library (read_csv)
            2. iterate dataframe to fetch user info
        '''
        try:
            df = pd.read_csv(file)

            users_to_add = []
            for idx, row in df.iterrows():
                # necessary columns are username, password, role
                new_user = User(
                    username=row["username"],
                    password=self.hash_passwd(row["password"]),
                    email=row.get("email") if pd.notna(row.get("email")) else None,
                    role=row["role"],
                    full_name=row.get("full_name") if pd.notna(row.get("full_name")) else None,
                    profile_picture=self.default_sticker,
                    message=None,
                    submission_count=0,
                    accepted_count=0,
                    rating=1500,
                    rank=None,
                )
                users_to_add.append(new_user)

            if users_to_add:
                self.session.add_all(users_to_add)
                self.session.commit()
        
        except pd.errors.EmptyDataError:
            print("The provided CSV file is empty or invalid.")
        except SQLAlchemyError as err:
            self.session.rollback()
            print(f"Database error occured: {err}")
