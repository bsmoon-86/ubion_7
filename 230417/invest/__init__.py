from invest.quant import momentum as mm
from invest.quant import buyandhold as bnh


class Invest:

    # 생성자 함수
    def __init__(self, _df, _col = 'Close', _start = '20100101', _end = '20230101'):
        self.df = _df
        self.col = _col
        self.start = _start
        self.end = _end

    def moment(self):
        self.df1 = mm.first(self.df, self.col, self.start, self.end)
        self.df2 = mm.second(self.df1)
        self.result = mm.third(self.df1, self.df2)
        return self.result
    
    def buy(self):
        self.result = bnh.bnh(self.df, self.col, self.start, self.end)
        return self.result