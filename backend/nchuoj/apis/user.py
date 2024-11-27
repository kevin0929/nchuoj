from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
)

from model.user import User
from model.utils.db import get_orm_session
from service.import_service import ImportService


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


@user_api.route("/<userid>/admin_index")
@jwt_required()
def admin_index(userid):
    '''manage user page
    '''
    try:
        session = get_orm_session()
        me = session.query(User).filter_by(userid=userid).first()
        users = session.query(User).order_by(User.userid).all()

        data = {
            "user": me.to_dict(),
            "users": [user.to_dict() for user in users],
        }

        return render_template("admin/users.html", **data)
    
    except Exception as err:
        print(f"Error fetching user data: {err}")

    return redirect(url_for("login_page"))


@user_api.route("/import", methods=["GET", "POST"])
@jwt_required()
def import_user():
    '''import csv file to create user in batches
    '''
    userid = get_jwt_identity()

    try:
        file = request.files.get("file")
        ImportService.import_user_by_csv(file)

        return jsonify({
            "redirectUrl": url_for("user_api.admin_index", userid=userid),
            "success": True,
        })

    except Exception as err:
        print(f"Error fetching user data: {err}")

    return jsonify({
        "redirectUrl": url_for("user_api.admin_index", userid=userid),
        "success": False
    })


@user_api.route("/add", methods=["GET", "POST"])
@jwt_required()
def add():
    '''add user by form format
    '''
    userid = get_jwt_identity()

    try:
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        full_name = request.form.get("fullname")
        role = request.form.get("role")

        # add user
        ImportService.add_user(
            username=username,
            password=password,
            email=email,
            role=role,
            full_name=full_name
        )

        return jsonify({
            "redirectUrl": url_for("user_api.admin_index", userid=userid),
            "success": True
        })

    except Exception as err:
        print(f"Error fetching user data: {err}")
    
    return jsonify({
            "redirectUrl": url_for("user_api.admin_index", userid=userid),
            "success": False
        })

