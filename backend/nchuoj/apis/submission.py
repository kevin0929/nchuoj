from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from model.problem import Problem
from model.submission import Submission
from model.utils.db import *


__all__ = ["submission_api"]

submission_api = Blueprint("submission_api", __name__)


@submission_api.route("/<userid>/<courseid>/submissions", methods=["GET"])
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
