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

                fig = go.Figure(data= [go.Scatter(
                                x = data['Date'],
                                 y =data['Close'],
                                 mode = 'lines',
                                 line = dict(color = flatly_colors['warning']),
                                 name= "Close price",
                                 showlegend=True)])
                
                fig.update_traces(line=dict(color=flatly_colors['success']))
        else:
                fig = go.Figure( data=[go.Candlestick(x=data['Date'],
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close'],
                        name= "Daily candles",
                        showlegend=True)])
                fig.update_layout(xaxis_rangeslider_visible=False)

        fig.update_layout(xaxis=dict(tickformat="%d.%m.%Y"))
        
        

        return fig

#depends in the prev function and dies ot build a plot from the ground up
def add_moving_average_traces(fig,df ,window_size_1 = None, window_size_2 = None):
    '''Take the figure from prev. function and add a moving average window if the user inputs one,
    do it for two possible windows,
    needs to check that old traces of MA are eliminated first
    ToDO: make this computationally more effective by checking if the input trace matches an existing one,
    Also toDO: the update triggeres too much but making it only only when the comp name changes might work. but comp cost is not too much right now'''
    
    traces_to_keep = []
    for trace in fig['data']:#look through the traces and keep the ones not showing the MA
        #The traces without names should always be kept
        if not isinstance(trace.name, str) or not trace.name.startswith('MA:'):
            traces_to_keep.append(trace)
    fig.data = traces_to_keep
    if isinstance(window_size_1, int):   
    
        fig.add_trace(go.Scatter(x = df['Date'],
                                 y =df['Close'].rolling(window_size_1).mean(),
                                 mode = 'lines',
                                 line = dict(color = flatly_colors['warning']),
                                 name= f'MA: {window_size_1}'))
    
    if isinstance(window_size_2, int):    
    
        fig.add_trace(go.Scatter(x = df['Date'],
                                 y =df['Close'].rolling(window_size_2).mean(),
                                 mode = 'lines',
                                 line = dict(color = flatly_colors['info']),
                                 name= f'MA: {window_size_2}'))
        
    return fig