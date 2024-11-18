from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.announcement import Announcement
from model.course import Course
from model.course_user import CourseUser
from model.homework import Homework
from model.problem import Problem
from model.submission import Submission
from model.user import User
from model.utils.db import *


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
