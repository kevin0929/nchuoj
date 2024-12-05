from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.announcement import Announcement
from model.course import Course
from model.course_user import CourseUser
from model.homework import Homework
from model.problem import Problem
from model.submission import Submission
from model.user import User
from model.utils.db import *
from service.course_service import CourseService


__all__ = ["course_api"]

course_api = Blueprint("course_api", __name__)


@course_api.route("/<userid>/list", methods=["GET"])
@jwt_required()
def index(userid):
    '''create course list index
    '''
    try:
        session = get_orm_session()
        user, _ = get_user_course(userid)
        courses = (
            session.query(Course)
            .join(CourseUser, Course.courseid == CourseUser.cu_id)
            .filter(CourseUser.userid == userid)
            .all()
        )

        # generate user index information
        data = {
            "user": user.to_dict(),
            "courses": [course.to_dict() for course in courses],
        }

        return render_template("user/courses.html", **data)

    except Exception as err:
        print(f"Error fetching user data: {err}")
    
    return "Error handling (not done yet)..."


@course_api.route("/<userid>/admin_index", methods=["GET", "POST"])
@jwt_required()
def admin_index(userid):
    '''manage course 
    '''
    try:
        session = get_orm_session()
        user, _ = get_user_course(userid)
        courses = session.query(Course).all()

        data = {
            "user": user.to_dict(),
            "courses": [course.to_dict() for course in courses],
        }

        return render_template("admin/courses.html", **data)

    except Exception as err:
        print(f"Error fetching user data: {err}")

    return redirect(url_for("login_page"))


@course_api.route("/add", methods=["GET", "POST"])
@jwt_required()
def add():
    '''add course
    '''
    me = get_jwt_identity()

    try:
        if request:
            coursename = request.form.get("coursename")
            teacher = request.form.get("teacher")
            start_date = request.form.get("start_date")
            end_date = request.form.get("end_date")
            is_activate = request.form.get("is_activate")

        CourseService.add_course(
            coursename=coursename,
            teacher=teacher,
            start_date=start_date,
            end_date=end_date,
            is_activate=is_activate
        )

        return jsonify({
            "redirectUrl": url_for("course_api.admin_index", userid=me),
            "success": True
        })

    except Exception as err:
        print(f"Error fetching user data: {err}")

    return redirect(url_for("login_page"))


@course_api.route("/<int:courseid>", methods=["DELETE"])
@jwt_required()
def delete(courseid):
    '''delete course by courseid
    '''
    me = get_jwt_identity()

    try:
        CourseService.delete_course(courseid)

        return jsonify({
            "redirectUrl": url_for("course_api.admin_index", userid=me),
            "success": True
        })

    except Exception as err:
        print(f"Error fetching user data: {err}")

    return redirect(url_for("login_page"))


@course_api.route("/<userid>/admin/<courseid>/edit")
@jwt_required()
def edit(userid, courseid):
    '''course edit page in course management
    '''
    me = get_jwt_identity()

    try:
        user, course = get_user_course(userid, courseid)
        print(user.to_dict())
        print(course.to_dict())

        data = {
            "user": user.to_dict(),
            "course": course.to_dict()
        }

        return render_template("/admin/course.html", **data)

    except Exception as err:
        print(f"Error fetching user data: {err}")

    return redirect(url_for("login_page"))
