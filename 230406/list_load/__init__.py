import pandas as pd
import os

# 함수의 형태로 폴더에 있는 파일들을 결합하는 함수 생성
def load(_dir, _end = '.csv'):
    # 매개변수 2개 생성 : _dir -> 파일의 경로
    #                   _end -> 파일의 확장자

    if not(_dir.endswith("/")):
        _dir = _dir+"/"

    if _end[0] != ".":
        _end = "." + _end

    # print(_dir, _end)

    # 파일의 리스트 호출
    file_list = os.listdir(_dir)
    # print(file_list)
    # 비어있는 데이터프레임 생성
    result = pd.DataFrame()
    # 파일 리스트에서 확장자가 같은 파일들만 결합
    for i in file_list:
        # 파일명의 확장자라는 인자값과 같은 경우
        if i.endswith(_end):
            print(i)
            # 확장자에 따른 read 함수 설정
            if _end == '.csv':
                df = pd.read_csv(_dir + i)
                result = pd.concat([result, df], axis=0, ignore_index=True)
            elif _end == ".json":
                df = pd.read_json(_dir + i)
                result = pd.concat([result, df], axis=0, ignore_index=True)
            elif _end in [".xlsx", ".xls"]:
                df = pd.read_excel(_dir + i)
                result = pd.concat([result, df], axis=0, ignore_index=True)
            else:
                return "지원하지 않는 확장자입니다."
    return result