from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_jwt_extended import (
    jwt_required, get_jwt_identity
)

from model.announcement import Announcement
from model.utils.db import *


__all__ = ["announcement_api"]

announcement_api = Blueprint("announcement_api", __name__)


@announcement_api.route("/<userid>/<courseid>/announcement", methods=["GET"])
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
