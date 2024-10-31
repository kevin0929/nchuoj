from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.announcement import Announcement
from model.course import Course
from model.course_user import CourseUser
from model.user import User
from model.utils.db import get_orm_session


__all__ = ["course_api"]

course_api = Blueprint("course_api", __name__)

@course_api.route("/<userid>/list", methods=["GET"])
@jwt_required()
def index(userid):
    '''create course list index
    '''
    try:
        session = get_orm_session()
        user = session.query(User).filter_by(userid=userid).first()
        courses = (
            session.query(Course)
            .join(CourseUser, Course.courseid == CourseUser.cu_id)
            .filter(CourseUser.userid == userid)
            .all()
        )

        # generate user index information
        user_info = user.to_dict()
        course_list = [course.to_dict() for course in courses]

        return render_template("user/courses.html", user=user_info, courses=course_list)

    except Exception as err:
        print(f"Error fetching user data: {err}")
    
    return "error"


@course_api.route("/<userid>/<courseid>/index")
@jwt_required()
def course(userid, courseid):
    '''course index
    '''
    try:
        session = get_orm_session()
        user = session.query(User).filter_by(userid=userid).first()

        user_info = user.to_dict()

        return render_template("user/course.html", user=user_info)

    except Exception as err:
        print(f"Error fetching user data: {err}")

    return "test"


@course_api.route("/<userid>/<courseid>/announcement")
@jwt_required()
def announcement(userid, courseid):
    '''announcements inside course
    '''
    try:
        session = get_orm_session()
        user = session.query(User).filter_by(userid=userid).first()
        announcements = session.query(Announcement).filter_by(courseid=courseid).all()

        user_info = user.to_dict()
        announcement_list = [announcement.to_dict() for announcement in announcements]

        return render_template("user/announcement.html", user=user_info, announcements=announcement_list)
    
    except Exception as err:
        return err
        print(f"Error fetching user data: {err}")
    
    return "test"
