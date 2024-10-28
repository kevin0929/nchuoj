import os
from flask import Flask, render_template, get_flashed_messages
from flask_jwt_extended import JWTManager
from datetime import timedelta

from apis import *


def app():
    app = Flask(__name__)
    app = setup_app(app)

    api2prefix = [(user_api, "/user")]
    for api, prefix in api2prefix:
        app.register_blueprint(api, url_prefix=prefix)

    return app


def setup_app(app):
    # session config
    app.config["SECRET_KEY"] = os.urandom(24)
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)

    # jwt config
    app.config["JWT_SECRET_KEY"] = "my_secert_key_should_in_environment"
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
    jwt = JWTManager()
    jwt.init_app(app)

    return app


app = app()


@app.route('/')
def login_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template("login.html", messages=messages)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1136)