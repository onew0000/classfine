from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 변경: 보안을 위해 실제 비밀키로 변경

DATA_FILE = "fines_data.json"
ADMIN_PASSWORD = '1234'  # 변경: 보안을 위해 실제 비밀번호로 변경

# 벌금 데이터를 파일에서 로드하는 함수
def load_data():
    if os.path.exists(DATA_FILE):  # 파일이 존재하는지 확인
        with open(DATA_FILE, "r") as file:
            return json.load(file)  # 파일에서 JSON 데이터를 로드
    return {}  # 파일이 없으면 빈 딕셔너리를 반환

# 벌금 데이터를 파일에 저장하는 함수
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)  # 데이터를 JSON 형식으로 파일에 저장

# 로그인 상태를 확인하는 데코레이터 함수
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:  # 세션에 'logged_in'이 없으면
            return redirect(url_for('login'))  # 로그인 페이지로 리다이렉트
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:  # 입력된 비밀번호가 관리자 비밀번호와 일치하면
            session['logged_in'] = True  # 세션에 'logged_in' 설정
            return redirect(url_for("index"))  # 메인 페이지로 리다이렉트
        else:
            flash("비밀번호가 틀렸습니다. 다시 시도하세요.")  # 비밀번호가 틀렸을 경우 플래시 메시지
    return render_template("login.html")  # 로그인 페이지 렌더링

@app.route("/logout")
def logout():
    session.pop('logged_in', None)  # 세션에서 'logged_in' 제거
    return redirect(url_for("index"))  # 메인 페이지로 리다이렉트

@app.route("/")
@login_required
def index():
    fines_data = load_data()  # 벌금 데이터 로드
    # 각 사람의 총 벌금 계산
    total_fines = {name: sum(fine['amount'] for fine in fines) for name, fines in fines_data.items()}
    return render_template("index.html", fines_data=fines_data, total_fines=total_fines)  # 메인 페이지 렌더링

@app.route("/add", methods=["POST"])
@login_required
def add_fine():
    fines_data = load_data()  # 벌금 데이터 로드
    name = request.form["name"]  # 폼에서 이름 추출
    amount = float(request.form["amount"])  # 폼에서 금액 추출 및 float로 변환
    reason = request.form["reason"]  # 폼에서 이유 추출
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 현재 시간 추출 및 포맷팅
    # 해당 이름의 벌금 데이터가 이미 존재하는지 확인
    if name in fines_data:
        fines_data[name].append({"amount": amount, "reason": reason, "timestamp": timestamp})  # 존재하면 추가
    else:
        fines_data[name] = [{"amount": amount, "reason": reason, "timestamp": timestamp}]  # 존재하지 않으면 새로 생성
    save_data(fines_data)  # 업데이트된 데이터 저장
    return redirect(url_for("index"))  # 메인 페이지로 리다이렉트

@app.route("/remove", methods=["POST"])
@login_required
def remove_fine():
    fines_data = load_data()  # 벌금 데이터 로드
    name = request.form["name"]  # 폼에서 이름 추출
    index = int(request.form["index"])  # 폼에서 인덱스 추출 및 int로 변환
    # 해당 이름의 벌금 데이터가 존재하는지 확인
    if name in fines_data:
        del fines_data[name][index]  # 해당 인덱스의 벌금 삭제
        if not fines_data[name]:  # 삭제 후 해당 이름의 벌금 데이터가 비었는지 확인
            del fines_data[name]  # 비었으면 해당 이름의 항목 전체 삭제
    save_data(fines_data)  # 업데이트된 데이터 저장
    return redirect(url_for("index"))  # 메인 페이지로 리다이렉트

if __name__ == "__main__":
    app.run(debug=True)  # Flask 앱 실행 (디버그 모드)
