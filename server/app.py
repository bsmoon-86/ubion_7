# 라이브러리 로드 
from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import json

# Flask 클래스 생성
# __name__ : 현재 파일의 이름
app = Flask(__name__)

# api 생성
# 네비게이션 함수
# 해당하는 주소로 요청이 들어왔을때 아래의 함수를 실행해준다. 
# localhost ( 127.0.0.1 ) -> 자기 자신의 컴퓨터
# localhost:3000/ 요청 시 아래의 함수를 실행
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/second")
def second():
    return render_template("second.html")

# post형태의 api 생성
@app.route("/login", methods=['post'])
def login():
    # 유저가 보낸 데이터를 변수에 대입
    # _id부분은 html에 input 안에 name이라는 속성의 값
    id = request.form['_id']
    password = request.form['_pass']
    print(id, password)
    if (id == "test") and (password == "1234"):
        return render_template("main.html", _id = id)
    else:
        return redirect("/")
    
@app.route("/corona")
def corona():
    # get형태에서 데이터를 받아서 변수에 대입 
    servicekey = request.args['servicekey']
    print(servicekey)
    if servicekey == "aaa":
        df = pd.read_csv("../csv/corona.csv")
        df = df.dropna(axis=0)
        dict_data = df.to_dict("records")
        return dict_data
    else:
        return "servicekey error"



app.run(host='0.0.0.0',port=3000)