




class FakeTicker:
    def __init__(self, ticker):
        self.info = {'regularMarketPrice': 1} if ticker == 'AAPL' else {}