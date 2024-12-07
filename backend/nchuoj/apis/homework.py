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
def homeworks(userid: int, courseid: int):
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
def homework(userid: int, courseid: int, homeworkid: int):
    '''homework info inside homework card be selected
    '''

    try:
        session = get_orm_session()
        user, course = get_user_course(userid, courseid)
        homework = session.query(Homework).filter_by(homeworkid=homeworkid).first()
        problems = session.query(Problem).filter_by(homeworkid=homeworkid).order_by(Problem.problemid).all()

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


@homework_api.route("/<userid>/admin/<courseid>/homeworks")
@jwt_required()
def admin_homeworks(userid: int, courseid: int):
    '''homeworks in the course (admin page)
    '''
    try:
        session = get_orm_session()
        user, course = get_user_course(userid, courseid)
        homeworks = session.query(Homework).filter_by(courseid=courseid).all()

        data = {
            "user": user.to_dict(),
            "course": course.to_dict(),
            "homeworks": [homework.to_dict() for homework in homeworks]
        }

        return render_template("admin/homeworks.html", **data)
    
    except Exception as err:
        print(f"Occur error: {err}")

    return "Error handling (not done yet)..."


@homework_api.route("/<userid>/admin/<courseid>/homework/<homeworkid>/edit")
@jwt_required()
def edit(userid: int, courseid: int, homeworkid: int):
    '''
    '''
    try:
        session = get_orm_session()
        user, course = get_user_course(userid, courseid)
        homework = session.query(Homework).filter(Homework.homeworkid == homeworkid).first()

        data = {
            "user": user.to_dict(),
            "course": course.to_dict(),
            "homework": homework.to_dict()
        }

        return render_template("admin/homework.html", **data)

    except Exception as err:
        print(f"Occur error: {err}")

    return "Error handling (not done yet)..."
