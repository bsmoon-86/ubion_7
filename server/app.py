# 라이브러리 로드 
from flask import Flask

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
    return "Hello World"

@app.route("/second")
def second():
    return "Second Page"



app.run(port=3000)