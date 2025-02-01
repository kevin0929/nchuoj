from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
)

from model.course_user import CourseUser
from model.course import Course
from model.user import User
from model.utils.db import get_orm_session


__all__ = ["course_user_api", ]

course_user_api = Blueprint("course_user_api", __name__)


@course_user_api.route("/<courseid>/index", methods=["GET"])
@jwt_required()
def index(courseid):
    '''create course user index in course
    '''
    try:
        userid = get_jwt_identity()

        session = get_orm_session()
        user = session.query(User).filter_by(userid=userid).first()
        course = session.query(Course).filter_by(courseid=courseid).first()

        results = (
            session.query(CourseUser, User)
            .join(User, CourseUser.userid == User.userid)
            .filter(CourseUser.courseid == courseid)
            .all()
        )

        course_users = []
        reserve_key = ["cu_id", "userid", "courseid", "username", "full_name", "role"]
        for course_user, user in results:
            # combine course_user and user into one dictionary
            combined_info = course_user.to_dict()
            combined_info.update(user.to_dict())

            # filter key to prevent leak important information
            filterd_dict = {k: combined_info.get(k) for k in reserve_key}
            course_users.append(filterd_dict)

        data = {
            "course_users": course_users,
            "user": user.to_dict(),
            "course": course.to_dict()
        }


        return render_template("admin/course_users.html", **data)

    except Exception as err:
        print(f"Occur error: {err}")

    return redirect(url_for("login_page"))
