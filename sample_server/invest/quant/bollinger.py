import pandas as pd
import numpy as np
from datetime import datetime

# 1번 함수 생성
# 매개 변수 추가 
def create_band(df, col = 'Close', start = '20100101', end = '20230101'):
    # 인덱스를 시계열로 변경
    if 'Date' in df.columns:
        df = df.set_index('Date')
    # start, end를 시계열로 변경
    start = datetime.strptime(start, '%Y%m%d').isoformat()
    end = datetime.strptime(end, '%Y%m%d').isoformat()
    # 결측치와 이상치를 제거 
    df = df.loc[~df.isin([np.nan, np.inf, -np.inf]).any(axis='columns'), [col]]
    # 수정 종가 컬럼을 제외한 데이터프레임 생성
    # df = df[[col]]
    # 이동 평균선 생성
    df['center'] = df.rolling(20).mean()
    # 상단 밴드 생성
    df['ub'] = df['center'] + ( 2 * df[col].rolling(20).std() )
    # 하단 밴드 생성
    df['lb'] = df['center'] - ( 2 * df[col].rolling(20).std() )
    # 데이터를 시작시간부터 종료 시간까지 필터
    df = df.loc[start:end]
    # 결과를 리턴
    return df

# 2번째 함수
def add_trade(df):
    # 기준이되는 컬럼이 무엇인가?
    # 기준이 되는 컬럼은 컬럼 중에 첫번째 이기 때문에 df.columns[0]
    col = df.columns[0]
    # trade 파생변수 생성
    df['trade'] = ""
    for i in df.index:
        # 상단 밴드보다 종가가 높은 경우
        if df.loc[i, col] > df.loc[i, 'ub']:
            # 현재 구매 상태이면
            if df.shift(1).loc[i, 'trade'] == 'buy':
                # 매도
                df.loc[i, 'trade'] = ''
            else:
                df.loc[i, 'trade'] = ''
        # 하단 밴드보다 종가가 낮은 경우
        elif df.loc[i, col] < df.loc[i, 'lb']:
            # 현재 구매 상태이면
            if df.shift(1).loc[i, 'trade'] == 'buy':
                # 구매 상태를 유지
                df.loc[i, 'trade'] = 'buy'
            else:
                # 매수
                df.loc[i, 'trade'] = 'buy' 
        else:
            # 현재 구매 상태이면
            if df.shift(1).loc[i, 'trade'] == 'buy':
                # 구매 상태를 유지
                df.loc[i, 'trade'] = 'buy'
            else:
                df.loc[i, 'trade'] = ''
    return df

# 3번째 함수 생성
def add_rtn(df):
    col = df.columns[0]
    # 수익율 파생변수 생성
    df['return'] = 1
    # 판매한 날의 수익율 대입
    rtn = 1.0
    buy = 0.0
    sell = 0.0

    for i in df.index:
        # 구매가를 출력
        if (df.shift(1).loc[i, 'trade'] == '') and \
            (df.loc[i, 'trade'] == 'buy'):
            buy = df.loc[i, col]
            # print('진입일 :', i, '구매 가격 :', buy)
        # 판매가를 출력
        elif (df.shift(1).loc[i, 'trade'] == 'buy') and \
            (df.loc[i, 'trade'] == ''):
            sell = df.loc[i, col]
            rtn = (sell - buy) / buy + 1
            df.loc[i, 'return'] = rtn
            # print('판매일 :', i, '판매 가격 :', sell, '수익율 :', rtn)

        # 구매가, 판매가를 초기화
        if df.loc[i, 'trade'] == '':
            buy = 0.0
            sell = 0.0
    
    # 누적 수익율 계산하여 파생변수에 대입
    acc_rtn = 1.0

    for i in df.index:
        rtn = df.loc[i, 'return']
        acc_rtn *= rtn
        df.loc[i, 'acc_rtn'] = acc_rtn

    # print('누적 수익율 :', acc_rtn)
    df.reset_index(inplace=True)
    return df
