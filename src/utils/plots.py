import plotly.express as px 
import plotly.graph_objects as go

import pandas as pd
import yfinance as yf
from utils.config import flatly_colors




def plot_stock_chart(data: pd.DataFrame, comp_name:str, ticker:str, metadata , chart_type:str):
        '''Plots the chart of a Stock as a Line, needs the input from a yfinane df
        to either display the opening or close prices, default will be the close prices '''
        
        
        try:
                y_name = f"Price in {metadata['currency']}"
        except:
                y_name = f"Price"
                
        if chart_type == 'line': 

                fig = px.line(data_frame= data,
                        x= 'Date',
                        y = 'Close',
                        labels = {'Close': y_name, 'Date': 'Date'}
                        )
                fig.update_traces(line=dict(color=flatly_colors['success']))
        else:
                fig = go.Figure( data=[go.Candlestick(x=data['Date'],
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'])])
                fig.update_layout(xaxis_rangeslider_visible=False)

        fig.update_layout(xaxis=dict(tickformat="%d.%m.%Y"))

        return fig