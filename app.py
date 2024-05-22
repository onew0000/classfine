from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 변경: 보안을 위해 실제 비밀키로 변경

DATA_FILE = "fines_data.json"
ADMIN_PASSWORD = '1234'  # 변경: 보안을 위해 실제 비밀번호로 변경

# 벌금 데이터 로드
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# 벌금 데이터 저장
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# 로그인 상태 확인 데코레이터
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for("index"))
        else:
            flash("비밀번호가 틀렸습니다. 다시 시도하세요.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for("index"))

@app.route("/")
@login_required
def index():
    fines_data = load_data()
    total_fines = {name: sum(fine['amount'] for fine in fines) for name, fines in fines_data.items()}
    return render_template("index.html", fines_data=fines_data, total_fines=total_fines)

@app.route("/add", methods=["POST"])
@login_required
def add_fine():
    fines_data = load_data()
    name = request.form["name"]
    amount = float(request.form["amount"])
    reason = request.form["reason"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if name in fines_data:
        fines_data[name].append({"amount": amount, "reason": reason, "timestamp": timestamp})
    else:
        fines_data[name] = [{"amount": amount, "reason": reason, "timestamp": timestamp}]
    save_data(fines_data)
    return redirect(url_for("index"))

@app.route("/remove", methods=["POST"])
@login_required
def remove_fine():
    fines_data = load_data()
    name = request.form["name"]
    index = int(request.form["index"])
    if name in fines_data:
        del fines_data[name][index]
        if not fines_data[name]:
            del fines_data[name]
    save_data(fines_data)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
