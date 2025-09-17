import yfinance as yf

def isin_ticker_to_ticker(ticker_isin:str):
    '''checks if the input is a ticker or Isin and returns the isin as a ticker for easy use with yfinance'''
    
    if len(ticker_isin) == 12:
        ticker = yf.Ticker(f'{ticker_isin}')
        return ticker.ticker
    else:
        return ticker_isin