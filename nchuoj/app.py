from flask import Flask, render_template, get_flashed_messages


app = Flask(__name__)


@app.route('/')
def login_page():
    messages = get_flashed_messages(with_categories=True)
    return render_template("login.html", messages=messages)


@app.route('/index')
def index():
    return render_template("user/index.html")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=1136)