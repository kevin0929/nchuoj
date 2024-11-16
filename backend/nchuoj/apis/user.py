from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
)

from model.user import User
from model.utils.db import get_orm_session


__all__ = ["user_api"]

user_api = Blueprint("user_api", __name__)

@user_api.route("/<userid>/index", methods=["GET"])
@jwt_required()
def index(userid):
    '''create user index
    '''
    try:
        session = get_orm_session()
        user = session.query(User).filter_by(userid=userid).first()

        if user is None:
            return "User not found", 404

        # generate user index information
        user_info = user.to_dict()

        return render_template("user/index.html", user=user_info)

    except Exception as err:
        print(f"Error fetching user data: {err}")
    
    return redirect(url_for("login_page"))
