import yfinance as yf
import pandas as pd
from cachetools import TTLCache, cached


def isin_ticker_to_ticker(ticker_isin:str):
    '''checks if the input is a ticker or Isin and returns the isin as a ticker for easy use with yfinance'''
    
    if len(ticker_isin) == 12:
        ticker = yf.Ticker(f'{ticker_isin}')
        return ticker.ticker
    else:
        return ticker_isin
 

_stock_cache = TTLCache(maxsize=10, ttl= 600)    
@cached(_stock_cache) 
def prepare_stock_data(ticker):
    '''Uses a Ticker, NOT ISIN to download the stock data and preprocesses it into the standard format expected by other functions'''
    
    data = yf.download(f'{ticker}', period = '5y')
    data.columns = data.columns.get_level_values(0) #get rid of the multi index for easier cashing
    data = data.reset_index()
   
    return data


def decode_records_data(data_records):
    '''uses the data saved as 'records' and decodes them int othe standard format of hte app.
    this is needed for cashed data. '''
    
    data = pd.DataFrame(data_records)
    data["Date"] = pd.to_datetime(data["Date"])
   
    return data