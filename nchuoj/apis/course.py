from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.course import Course
from model.user import User
from model.utils.db import get_orm_session


__all__ = ["course_api"]

course_api = Blueprint("course_api", __name__)

@course_api.route("/<userid>/index", methods=["GET"])
@jwt_required()
def index(userid):
    '''create course list index
    '''
    test_error = ""
    try:
        '''
        TODO:
            1. We need courseuser table.
            2. List all available courses for user.
        '''
        session = get_orm_session()
        user = session.query(User).filter_by(userid=userid).first()
        courses = session.query(Course).all()

        # generate user index information
        user_info = user.to_dict()
        course_list = [course.to_dict() for course in courses]

        return render_template("user/course.html", user=user_info, courses=course_list)

    except Exception as err:
        print(f"Error fetching user data: {err}")
    
    return "error"
