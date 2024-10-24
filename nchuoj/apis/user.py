from flask import Blueprint, render_template


__all__ = ["user_api"]

user_api = Blueprint("user_api", __name__)


@user_api.route("/", methods=["GET"])
def user_index():
    '''create user index
    '''
    return render_template("user/index.html")

    