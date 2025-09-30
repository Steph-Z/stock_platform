import yfinance as yf
import pandas as pd
from cachetools import TTLCache, cached
import re


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

_stock_cache = TTLCache(maxsize=10, ttl= 600)    
def get_stock_metadata(ticker):
    '''downloads the metadata of the stock to display currency, names etc. grouped into one call to save resources'''
    stock_metadata = yf.Ticker(ticker).info
    
    return stock_metadata


def decode_records_data(data_records):
    '''uses the data saved as 'records' and decodes them int othe standard format of hte app.
    this is needed for cashed data. '''
    
    data = pd.DataFrame(data_records)
    data["Date"] = pd.to_datetime(data["Date"])
   
    return data

def clean_comp_name(comp_name:str):
    '''finds trailing letters behind company names to make naming more robust for international companies'''
    #split name and put back together using single spaces
    comp_name = " ".join(comp_name.split())
    # remove single characters at the end 
    comp_name = re.sub(r"\s+[A-Z0-9]$", "", comp_name)
    
    return comp_name


def add_currency_information(x, currency):
    '''adds the currency information to the entries of a df based on the metadata'''
    if currency == "USD":
        return f"${x:,.2f}"
    elif currency == "EUR":
        return f"{x:,.2f} €"
    else:
        return f"{x:,.2f} {currency}"
    
def prepare_data_for_llm(data):
    '''takes the standard data, decoded and returns the llm output'''
    
    data_change = pd.DataFrame(data['Close'].values, 
                               index=data['Date'], 
                               columns=['Close'])
    data_change['Change from prev_day in %'] = data_change['Close'].pct_change() * 100
    data_change.drop('Close',axis = 1, inplace= True)
    data_change.dropna(inplace= True)
    data_change = data_change.round(1)
    
    return data_change.to_csv(index= True, header= False).strip()