import os
from flask import Flask, render_template, get_flashed_messages
from datetime import timedelta

from apis import *


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)


api2prefix = [(user_api, "/user")]
for api, prefix in api2prefix:
    app.register_blueprint(api, url_prefix=prefix)


@app.route('/')
def login_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template("login.html", messages=messages)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1136)