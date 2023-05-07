## flask 로드 
from flask import Flask, render_template, request
import pandas as pd
import invest

## Class 생성
app = Flask(__name__)

## localhost:3000/ 요청시 index.html 리턴 api 생성
@app.route("/")
def index():
    # inex.html 그래프를 그리기 위해서 필요한 변수 값 
    # x_pos, y_pos 
    # 코로나 데이터를 로드
    # 일일 확진자 파생변수
    # x축에는 등록일시
    # y축에는 일일확진자
    df = pd.read_csv("../csv/corona.csv")
    df.columns = ["인덱스", "등록일시", "사망자", "확진자", "게시글번호", 
                    "기준일", "기준시간", "수정일시", "누적의심자", 
                    "누적확진률"]
    df.sort_values("등록일시", inplace=True)
    df["일일확진자"] = df["확진자"].diff().fillna(0)
    df_2 = df.tail(100)
    _x = df_2["등록일시"].tolist()
    _y = df_2["일일확진자"].tolist()
    data = df_2.to_dict()
    cnt = len(df_2)
    columns = df_2.columns  # 데이터형 list
    label =  '일일확진자'
    # print(data)
    # _x = [1,2,3,4,5]
    # _y = [40, 20, 10, 40, 100]
    return render_template("index.html", 
                            x_pos=_x, 
                            y_pos=_y, 
                            cnt = cnt, 
                            data = data, 
                            columns = columns, 
                            name = label)

@app.route("/index2")
def index2():
    df = pd.read_csv("../csv/corona.csv")
    df.columns = ["인덱스", "등록일시", "사망자", "확진자", "게시글번호", 
                    "기준일", "기준시간", "수정일시", "누적의심자", 
                    "누적확진률"]
    df.sort_values("등록일시", inplace=True)
    df["일일확진자"] = df["확진자"].diff().fillna(0)
    df["일일사망자"] = df["사망자"].diff().fillna(0)
    df_2 = df.tail(50)
    _x = df_2["등록일시"].tolist()
    _y = df_2["일일사망자"].tolist()
    data = df_2.to_dict()
    cnt = len(df_2)
    columns = df_2.columns  # 데이터형 list
    c_cnt = len(columns)
    # print(data)
    # _x = [1,2,3,4,5]
    # _y = [40, 20, 10, 40, 100]
    return render_template("index2.html", 
                            x_pos=_x, 
                            y_pos=_y, 
                            cnt = cnt, 
                            data = data, 
                            c_cnt = c_cnt, 
                            columns = columns)

@app.route("/invest")
def test():
    file_name = request.args['file']
    invest_type = request.args['type']
    print(file_name, invest_type)
    df = pd.read_csv(f"../csv/{file_name}.csv", index_col='Date')
    invest_class = invest.Invest(df)
    if invest_type == 'buyandhold':
        result = invest_class.buyandhold()
    elif invest_type == 'bollinger':
        result = invest_class.bollinger()
    else:
        result = invest_class.momentum()
    _x = result['Date'].tolist()
    _y = result['acc_rtn'].tolist()
    cnt = len(result)
    columns = result.columns
    data = result.to_dict(orient='records')
    label = '누적수익율'
    print("column : ", columns)
    print("DATA :",  result.head(5).to_dict(orient='records'))
    return render_template('index.html', 
                           x_pos = _x, 
                           y_pos = _y, 
                           cnt = cnt, 
                           data = data, 
                           columns = columns, 
                           name = label)

app.run(port=3000)