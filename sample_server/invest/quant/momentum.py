import pandas as pd
import numpy as np
from datetime import datetime

# 1번 함수 생성
def first(df, col = 'Close', start = '20100101', end = '20230101'):
    # 인덱스가 Date가 아니면? Date컬럼을 인덱스로 변경
    if 'Date' in df.columns:
        df = df.set_index('Date')
    # start, end를 시계열로 변경
    start = datetime.strptime(start, '%Y%m%d').isoformat()
    end = datetime.strptime(end, '%Y%m%d').isoformat()
    # 결측치와 이상치를 제거
    df = df.loc[~df.isin([np.nan, np.inf, -np.inf]).any(axis='columns')]
    # 수정종가를 제외한 나머지 컬럼 삭제
    df = df[[col]]
    # 인덱스를 시계열로 변경
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d')
    df = df.loc[start:end]
    # STD-YM 컬럼을 생성 
    df['STD-YM'] = list(map(lambda x : datetime.strftime(x, '%Y-%m'), df.index))

    return df

# 2번함수 
def second(df):
    col = df.columns[0]
    # df2 = pd.DataFrame()

    # _list = df['STD-YM'].unique()

    # for i in _list:
    #     last_df = df.loc[df['STD-YM'] == i].tail(1)
    #     df2 = pd.concat([df2, last_df])

    # 월별 마지막날의 데이터만 추출
    df2 = df.loc[df['STD-YM'] != df.shift(-1)['STD-YM']]
    
    # 전 월, 전년도의 종가 파생변수 생성
    df2['BF_1M'] = df2.shift(1)[col].fillna(0)
    df2['BF_12M'] = df2.shift(12)[col].fillna(0)

    return df2


# 3번 함수
def third(df1, df2):
    df1['trade'] = ""
    df1['return'] = 1
    col = df1.columns[0]

    for i in df2.index:
        signal = ""

        momentum_index = df2.loc[i, 'BF_1M'] / df2.loc[i, 'BF_12M'] - 1

        flag = True if((momentum_index > 0) \
                and (momentum_index != np.inf) \
                and (momentum_index != -np.inf)) else False
        
        if flag : 
            signal = 'buy'
        
        df1.loc[i, 'trade'] = signal
    
    rtn = 1.0
    buy = 0
    sell = 0

    for i in df1.index:
        if (df1.loc[i, 'trade'] == "buy") and (df1.shift(1).loc[i, 'trade'] == ""):
            buy = df1.loc[i, col]
            print('구입일 :', i, "구입 가격 :", buy)
        elif (df1.loc[i, 'trade'] == "") and (df1.shift(1).loc[i, 'trade'] == "buy"):
            sell = df1.loc[i, col]
            print('판매일 :', i, "판매 가격 :", sell)
            rtn = (sell - buy) / buy + 1
            df1.loc[i, 'return'] = rtn
    

    acc_rtn = 1.0

    for i in df1.index:
        acc_rtn *= df1.loc[i, 'return']
        df1.loc[i, 'acc_rtn'] = acc_rtn
    print(acc_rtn)
    df1.reset_index(inplace=True)

    return df1
