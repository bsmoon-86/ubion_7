import numpy as np
from datetime import datetime
import pandas as pd

def bnh(df, column = 'Close', start = '20000101', end = '20200101'):
    # 인덱스 시계열로 변경
    df.index = pd.to_datetime(df.index)
    start = datetime.strptime(start, '%Y%m%d')
    end = datetime.strptime(end, '%Y%m%d')
    df = df.loc[start : end]
    # 결측치, 무한대 제외
    df = df.loc[~df.isin([np.nan, np.inf, -np.inf]).any(axis='columns')]
    # 수정 종가만 있는 데이터프레임으로 변경
    df = df[[column]] 
    # 일별 수익율 변수 생성
    df['daily_rtn'] = df[column].pct_change()
    # 누적 수입율 변수 생성
    df['st_rtn'] = (1 + df['daily_rtn']).cumprod()
    # 인덱스의 타입을 문자열로 변경
    df.index = df.index.astype('str')
    # 인덱스를 리셋 기존의 인덱스는 유지
    df.reset_index(inplace=True)
    # 데이터프레임을 리턴
    return df
