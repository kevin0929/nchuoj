from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.announcement import Announcement
from model.course import Course
from model.course_user import CourseUser
from model.homework import Homework
from model.problem import Problem
from model.submission import Submission
from model.user import User
from model.utils.db import get_orm_session


__all__ = ["course_api"]

course_api = Blueprint("course_api", __name__)


def get_user_course(userid, courseid=None):
    session = get_orm_session()
    user = session.query(User).filter_by(userid=userid).first()
    course = session.query(Course).filter_by(courseid=courseid).first() if courseid else None

    if not user or (courseid and not course):
        abort(404)

    return user, course


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


"""
''' 
TODO : 
    1. When user first enter this course, what will he see?
'''

@course_api.route("/<userid>/<courseid>/index")
@jwt_required()
def course(userid, courseid):
    '''course index
    '''
    try:
        session = get_orm_session()
        user = session.query(User).filter_by(userid=userid).first()

        user_info = user.to_dict()

        return render_template("user/course.html", user=user_info, courseid=courseid)

    except Exception as err:
        print(f"Error fetching user data: {err}")

    return "Error handling (not done yet)..."
"""


@course_api.route("/<userid>/<courseid>/announcement", methods=["GET"])
@jwt_required()
def announcement(userid, courseid):
    '''announcements inside course
    '''
    try:
        session = get_orm_session()
        user, course = get_user_course(userid, courseid)
        announcements = session.query(Announcement).filter_by(courseid=courseid).all()

        data = {
            "user": user.to_dict(),
            "course": course.to_dict(),
            "announcements": [announcement.to_dict() for announcement in announcements],
        }

        return render_template("user/announcement.html", **data)
    
    except Exception as err:
        print(f"Error fetching user data: {err}")
    
    return "Error handling (not done yet)..."


@course_api.route("/<userid>/<courseid>/homeworks", methods=["GET"])
@jwt_required()
def homeworks(userid, courseid):
    '''homeworks inside course
    '''

    try:
        session = get_orm_session()
        user, course = get_user_course(userid, courseid)
        homeworks = session.query(Homework).filter_by(courseid=courseid).all()

        data = {
            "user": user.to_dict(),
            "course": course.to_dict(),
            "homeworks": [homework.to_dict() for homework in homeworks],
        }

        return render_template("user/homeworks.html", **data)
    
    except Exception as err:
        print(f"Error fetching user data: {err}")

    return "Error handling (not done yet)..."


@course_api.route("/<userid>/<courseid>/submissions", methods=["GET"])
@jwt_required()
def submissions(userid, courseid):
    try:
        session = get_orm_session()
        user, course = get_user_course(userid, courseid)
        submissions = (
            session.query(Submission, Problem)
            .join(Problem, Submission.problemid == Problem.problemid)
            .filter(Submission.userid == userid)
            .all()
        )

        submission_data = [
            {
                "submission": submission.to_dict(),
                "problem": problem.to_dict()
            }
            for submission, problem in submissions
        ]
        
        data = {
            "user": user.to_dict(),
            "course": course.to_dict(),
            "submissions": submission_data[::-1]
        }

        return render_template("user/submissions.html", **data)

    except Exception as err:
        print(f"Error fetching user data: {err}")

    return "Error handling (not done yet)..."


@course_api.route("/<userid>/<courseid>/homework/<homeworkid>", methods=["GET"])
@jwt_required()
def homework(userid, courseid, homeworkid):
    '''homework info inside homework card be selected
    '''

    try:
        session = get_orm_session()
        user, course = get_user_course(userid, courseid)
        homework = session.query(Homework).filter_by(homeworkid=homeworkid).first()
        problems = session.query(Problem).filter_by(homeworkid=homeworkid).all()

        data = {
            "user": user.to_dict(),
            "course": course.to_dict(),
            "homework": homework.to_dict(),
            "problems": [problem.to_dict() for problem in problems]
        }

        return render_template("user/homework.html", **data)
    
    except Exception as err:
        print(f"Error fetching user data: {err}")

    return "Error handling (not done yet)..."


@course_api.route("/<userid>/<courseid>/homework/<homeworkid>/<problemid>")
@jwt_required()
def problem(userid, courseid, homeworkid, problemid):
    '''problem inside homework
    '''

    try:
        session = get_orm_session()
        user, course = get_user_course(userid, courseid)
        homework = session.query(Homework).filter_by(homeworkid=homeworkid).first()
        problem = session.query(Problem).filter_by(problemid=problemid).first()

        data = {
            "user": user.to_dict(),
            "course": course.to_dict(),
            "homework": homework.to_dict(),
            "problem": problem.to_dict()
        }

        return render_template("user/problem.html", **data)
    
    except Exception as err:
        print(f"Error fetching user data: {err}")
    
    return "Error handling (not done yet)..."
