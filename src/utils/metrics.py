import pandas as pd
import yfinance as yf




def calculate_volatility(timeframe:tuple, data:pd.DataFrame, ticker: str):
    '''This function calculates the volatility of a Stock for a given start and end date given by a tuple (start, end)
    in the format 'year-month-date', includes start state, omits end date '''
    
    data_adjusted = data['Close'].loc[(data.index >= timeframe[0]) & (data.index < timeframe[1])]
    
    vola_timeframe = data_adjusted.std() #already uses degrees of freedom
    
    return vola_timeframe, len(data_adjusted) #we could round but we can also have this as exact number and only round for the displayed output