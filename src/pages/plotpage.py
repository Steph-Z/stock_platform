from dash import html, dcc, Input, Output, callback, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

from utils.isin_ticker_checkups import check_isin_ticker_input, input_case_insensitive, remove_dashes
from utils.plots import plot_stock_chart_line
from utils.misc import colors
from utils.transforms import decode_records_data


def layout():
    '''genral layout of the plotting page '''
    return html.Div(
        [
        html.H2('Stock Charts', style= {'textAlign': 'center'}),
        
        dcc.Graph(id= 'stocklineplot', figure= {})
        ]
    )
    
#Callback to update the plot bassed on the selected stock and data 
@callback(
    Output('stocklineplot', 'figure'),
    Input('Stockselection', 'value'),
    Input('stockdata', 'data')
)
def update_stock_plot(stock_input_value, stock_data_records):
    
    if not stock_input_value or not stock_data_records:
        return {}
    
    df =decode_records_data(stock_data_records)
    fig = plot_stock_chart_line(df, ticker= stock_input_value)
    
     # Apply consistent color scheme
    fig.update_layout(
        xaxis=dict(gridcolor=colors['chart_gridcolor']),
        yaxis=dict(gridcolor=colors['chart_gridcolor'])
    )

    return fig