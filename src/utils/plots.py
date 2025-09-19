import plotly.express as px 
import pandas as pd
import yfinance as yf



def plot_stock_chart_line(data: pd.DataFrame, ticker):
    '''Plots the chart of a Stock as a Line, needs the input from a yfinane df
    to either display the opening or close prices, default will be the close prices '''
    y_name = f"Price in {yf.Ticker(ticker).info['currency']}"
    comp_name = yf.Ticker(ticker).info['displayName']
    
    fig = px.line(data_frame= data,
            x= 'Date',
            y = 'Close',
            labels = {'Close': y_name, 'Date': 'Date'})
    
    fig.update_layout(title= {"text": f'Chart of the {comp_name} Stock', "font":{"size": 20}, "x": 0.5, "y":0.95, "xanchor": "center", "yanchor": "top"})
    
    return fig