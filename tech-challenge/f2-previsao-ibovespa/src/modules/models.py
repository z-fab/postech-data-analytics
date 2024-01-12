class IBovespaData:

    def __init__(self, date, open, high, low, close) -> None:
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close

class PredictIbovespa:

    def __init__(self, date, predict) -> None:
        self.date = date
        self.predict = predict

class Consolidate:

    def __init__(self, date, close, predict) -> None:
        self.date = date
        self.close = close
        self.predict = predict
        self.diff = close - predict
        self.diff_percent = (self.diff / self.close) * 100 if self.close > 0 else 0
