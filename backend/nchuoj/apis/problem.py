from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.problem import Problem
from model.utils.db import get_orm_session


__all__ = ["problem_api", ]

problem_api = Blueprint("problem_api", __name__)

@problem_api.route("/<problemid>/submit", methods=["POST"])
def submit(problemid):
    '''submit solution to problem
    '''
    try:
        type = request.form.get("type")
        lang = request.form.get("language")
        success = False     # just temp flag

        if type == "code":
            code = request.form.get("code")
            success = True
            print(code)
        elif type == "file":
            file = request.files.get("content")
            success = True
            if file:
                print(f"Received file submission for problem {problemid}: {lang}, {file.filename}")

    except Exception as err:
        return jsonify({"msg": err, "success": False})

    return jsonify({"msg": "yes", "success": success})
