import yfinance as yf
import pandas as pd
import plotly.express as px 

from utils.metrics import calculate_volatility
from utils.plots import plot_stock_chart_line
from utils.transforms import isin_ticker_to_ticker

ticker = 'AAPL'
ticker = isin_ticker_to_ticker(ticker)
    
data = yf.download(f'{ticker}', period = 'max')
    
fig = plot_stock_chart_line(data = data.Close, ticker = ticker)
fig.show(renderer = 'browser')