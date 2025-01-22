from datetime import datetime, timezone, timedelta
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)
from flask_jwt_extended import jwt_required, get_jwt_identity

from model.homework import Homework
from model.problem import Problem
from model.submission import Submission
from model.testcase import Testcase
from model.user_problem_score import UserProblemScore
from model.utils.db import *
from service.problem_service import ProblemService
from service.submit_service import SubmitService


__all__ = ["problem_api", ]

problem_api = Blueprint("problem_api", __name__)


@problem_api.route("/<userid>/<courseid>/homework/<homeworkid>/<problemid>")
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


@problem_api.route("/<userid>/admin/<courseid>/homework/<homeworkid>/problems")
@jwt_required()
def admin_problems(userid: int, courseid: int, homeworkid: int):
    '''
    '''
    try:
        session = get_orm_session()
        user, course = get_user_course(userid, courseid)
        homework = session.query(Homework).filter(Homework.homeworkid == homeworkid).first()
        problems = session.query(Problem).filter(Problem.homeworkid == homeworkid).all()

        data = {
            "user": user.to_dict(),
            "course": course.to_dict(),
            "homework": homework.to_dict(),
            "problems": [problem.to_dict() for problem in problems]
        }

        return render_template("admin/problems.html", **data)
    
    except Exception as err:
        print(f"Occur error: {err}")

    return "Error handling (not done yet)..."


@problem_api.route("/<userid>/admin/<courseid>/homework/<homeworkid>/add", methods=["GET", "POST"])
@jwt_required()
def add(userid: int, courseid: int, homeworkid: int):
    '''add problem page
    '''
    try:
        session = get_orm_session()
        user, course = get_user_course(userid, courseid)
        homework = session.query(Homework).filter(Homework.homeworkid == homeworkid).first()

        # convert user / course / homework to dict and make a summary dict
        data_user = user.to_dict()
        data_course = course.to_dict()
        data_homework = homework.to_dict()
        
        data = {
            "userid": data_user["userid"], # for url
            "courseid": data_course["courseid"],
            "homeworkid": data_homework["homeworkid"],
            "user": data_user, # for render page
            "course": data_course,
            "homeworks": data_homework
        }

        if request.method == "POST":
            new_problem_info = {key: value for key, value in request.form.items()}
            new_problem_info["is_show"] = True

            if "testcase" in request.files:
                testcases = request.files.get("testcase")
                resp = ProblemService.add_problem(
                    new_problem_info,
                    testcases,
                )

                # flash msg and back to problems page
                if resp["status"] == "success":
                    flash(resp["msg"], "success")
                else:
                    flash(resp["msg"], "error")
                
                return redirect(url_for("problem_api.admin_problems", **data))
            
            flash("Please upload testcase zip file", "error")
            return redirect(url_for("problem_api.admin_problems", **data))

        return render_template("admin/problem_add.html", **data)

    except Exception as err:
        print(f"Occur error: {err}")

    return "Error handling (not done yet)..."


@problem_api.route("/<userid>/admin/<courseid>/homework/<homeworkid>/<problemid>/edit")
@jwt_required()
def edit(userid: int, courseid: int, homeworkid: int):
    '''edit problem
    '''
    pass


@problem_api.route("/<userid>/admin/<courseid>/homework/<homeworkid>/<problemid>", methods=["delete"])
@jwt_required()
def delete(
    userid: int,
    courseid: int,
    homeworkid: int,
    problemid: int
):
    '''delete problem
    '''
    param = {
        "userid": userid,
        "courseid": courseid,
        "homeworkid": homeworkid,
    }

    try:
        ProblemService.delete_problem(problemid=problemid)

        return jsonify({
            "redirectUrl": url_for("problem_api.admin_problems", **param),
            "success": True
        })

    except Exception as err:
        print(f"Error fetching user data: {err}")

    return jsonify({
        "redirectUrl": url_for("problem_api.admin_problems", **param),
        "success": False
    })



@problem_api.route("/<problemid>/submit", methods=["GET", "POST"])
@jwt_required()
def submit(problemid): 
    '''
        1. handle form request
        2. query testcase with problemid and prepare payload
        3. get submit service and do submit method
        4. receive, decode response and make new submission commit to db 
        5. redirect to submission page
    '''
    try:
        type = request.form.get("type")
        lang = request.form.get("language")
        courseid = request.form.get("courseid")

        session = get_orm_session()
        testcases_list = session.query(Testcase).filter_by(problemid=problemid).all()
        testcases = [testcase.to_dict() for testcase in testcases_list]
        problem = session.query(Problem).filter_by(problemid=problemid).first().to_dict()

        submit_service = SubmitService()

        if type == "code":
            source_code = request.form.get("code")
        elif type == "file":
            file = request.files.get("content")
            if file:
                source_code = file.read().decode("utf-8")

        # get language id and make payload, submit
        langid = submit_service.get_language_id(lang)
        memory_limit = problem["memory_limit"]
        cpu_time_limit = problem["runtime_limit"]

        resp = submit_service.submit(
            langid=langid,
            source_code=source_code,
            memory_limit=memory_limit,
            cpu_time_limit=cpu_time_limit,
            testcases=testcases
        )

        # prepare parameter
        runtime = resp["execute_time"]
        memory = resp["memory_usage"]
        status = resp["status"]
        score = problem["score"]
        submit_time = datetime.now(timezone(timedelta(hours=8)))
        userid = get_jwt_identity()

        # create submission and score interface and sumbit to database
        if (runtime is not None) and (memory is not None) and status:
            # submission
            new_submission = Submission(
                userid=userid,
                problemid=problemid,
                runtime=runtime,
                memory=memory,
                score=score if status == "Accepted" else 0,
                language=lang,
                status=status,
                submit_time=submit_time
            )
            session.add(new_submission)

            # user problem score
            check_score = session.query(UserProblemScore).filter_by(userid=userid, problemid=problem["problemid"]).first()
            if check_score:
                if check_score.status != "AC":
                    if resp["short_status"] == "AC":
                        check_score.score = 100
                        check_score.status = "AC"
                    else:
                        check_score.status = resp["short_status"]
            else:
                new_score = UserProblemScore(
                    userid=userid,
                    problemid=problem["problemid"],
                    score=100 if resp["short_status"] == "AC" else 0,
                    status=resp["short_status"]
                ) 
                session.add(new_score)

            session.commit()

        session.close()

        return {
            "redirectUrl": url_for("submission_api.submissions", userid=userid, courseid=courseid),
            "success": True,
        }

    except Exception as err:
        return jsonify({"msg": err, "success": False})

    return jsonify({"msg": "yes", "success": True})
