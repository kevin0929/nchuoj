from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.testcase import Testcase
from model.utils.db import get_orm_session
from service.submit import SubmitService


__all__ = ["problem_api", ]

problem_api = Blueprint("problem_api", __name__)

@problem_api.route("/<problemid>/submit", methods=["POST"])
def submit(problemid): 
    '''
        1. handle form request
        2. query testcase with problemid and prepare payload
        3. get submit service and do submit method
        4. receive response and redirect to submission page
    '''
    try:
        type = request.form.get("type")
        lang = request.form.get("language")

        session = get_orm_session()
        testcases_list = session.query(Testcase).filter_by(problemid=problemid).all()
        testcases = [testcase.to_dict() for testcase in testcases_list]

        submit_service = SubmitService()

        if type == "code":
            source_code = request.form.get("code")
        elif type == "file":
            file = request.files.get("content")
            if file:
                source_code = file.read().decode("utf-8")

        # get language id and make payload, submit
        langid = submit_service.get_language_id(lang)
        resp = submit_service.submit(
            langid=langid,
            source_code=source_code,
            testcases=testcases
        )

        # decode resp
        execute_time = resp["execute_time"]
        memory_usage = resp["memory_usage"]
        status = resp["status"]

    except Exception as err:
        return jsonify({"msg": err, "success": False})

    return jsonify({"msg": "yes", "success": True})
