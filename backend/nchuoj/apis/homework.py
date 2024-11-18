from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from model.homework import Homework
from model.problem import Problem
from model.utils.db import *


__all__ = ["homework_api"]

homework_api = Blueprint("homework_api", __name__)


@homework_api.route("/<userid>/<courseid>/homeworks", methods=["GET"])
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


@homework_api.route("/<userid>/<courseid>/homework/<homeworkid>", methods=["GET"])
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
