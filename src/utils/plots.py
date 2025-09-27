import plotly.express as px 
import plotly.graph_objects as go

import pandas as pd
import yfinance as yf




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
                        labels = {'Close': y_name, 'Date': 'Date'})
        else:
                fig = go.Figure( data=[go.Candlestick(x=data['Date'],
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'])])
                fig.update_layout(xaxis_rangeslider_visible=False)


        #fig.update_layout(title= {"text": f'Chart of the {comp_name} Stock', "font":{"size": 20}, "x": 0.5, "y":0.95, "xanchor": "center", "yanchor": "top"})

        return fig