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



@user_api.route("/login", methods=["POST"])
def login():
    '''handle user login request
    '''

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not (username and password):
            flash("Username and password are required.", "error")
            return redirect(url_for("login_page"))

        try:
            session = get_orm_session()
            user = session.query(User).filter_by(username=username).first()

            if not user:
                flash("Invalid username or password.", "error")
                return redirect(url_for("login_page"))

            '''
            TODO:
                1. password need to be hashed
            '''

            if password == user.password:
                # generate user's jwt and store it into Cookie
                access_token = create_access_token(identity=user.userid)
                response = redirect(url_for("user_api.index", userid=user.userid))
                set_access_cookies(response, access_token)

                return response
            else:
                flash("Invalid username or password.", "error")
                return redirect(url_for("login_page"))

        except Exception as err:
            print(f"Error during login: {err}")
            flash("An error occurred during login.", "error")
    
    return redirect(url_for("login_page"))


# @app.route("/logout", methods=["GET"])
# @jwt_required()
# def logout():
#     '''unset jwt token from cookie and redirect to login page
#     '''

#     response = redirect(url_for("login_page"))
#     unset_access_cookies(response)

#     return response
