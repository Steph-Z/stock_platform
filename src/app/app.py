import yfinance as yf
import pandas as pd
import plotly.express as px 
from dash import Dash, dcc, html, Input, Output, callback

from utils.metrics import calculate_volatility
from utils.plots import plot_stock_chart_line
from utils.transforms import isin_ticker_to_ticker, prepare_stock_data,  decode_records_data
from utils.misc import create_navbar
#Initializing the app

app = Dash()
app.title = "Stock Dashboard"

#########Color settings

colors = {    'background': "#FFFFFF",
        'input_background': "#FFFFFFFF", #some input boxes cant handle a different color so white is a kind of given to avoid a lot of custom code (i dont fancy doing css here)
        'chart_background': "#ffffff",
        'chart_gridcolor':'#727272',
        'text': "#000000"
}


#We have to define the layout now

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1('Stock Dashboard',#as a header
    style={
            'textAlign': 'center',
            'color': colors['text']
        } 
    ),
                      
    dcc.Input(
        id = 'Stockselection',
        placeholder = "Enter a Ticker or ISIN",
        type = 'text',
        value = 'US0378331005',
        debounce= True,
        style={
        'textAlign': 'center',
        'color': colors['text'],
        'backgroundColor': colors['input_background']
        }), 
    
    #Store the data so I can acess it in multiple callbacks
    
    dcc.Store(id = 'stock-data'),  
    #Plot
    dcc.Graph(figure = {}, id = 'stockchart'),
    
    dcc.DatePickerRange(
        id= 'Daterange',
        start_date = '2025-08-01',
        end_date = '2025-09-01',
        style={
        'textAlign': 'center',
        'color': colors['text'],
        'backgroundColor': colors['input_background']
        }),
    #Volatility text
    html.Div(id = 'volatility-custom-timeframe', style = {"fontSize": "20px", "marginTop": "20px"})
])

#Connect the LAyout to the functions
#Callback for chat/stock data 
@callback(
        Output(component_id = 'stockchart', component_property = "figure"), #always the id of the compoent and then the property, they are fixed
        Output('stock-data', 'data' ),
        Input('Stockselection', "value")
)


def update_data_and_plot(ticker):    

    ticker = isin_ticker_to_ticker(ticker)
    data = prepare_stock_data(ticker)
        
    
    #get the figure 
    fig = plot_stock_chart_line(data = data, ticker = ticker)
    #change colors of the figure to match the layout
    fig.update_layout(
    plot_bgcolor=colors['chart_background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'],
    xaxis=dict(gridcolor= colors['chart_gridcolor']),  # Set gridline color for x-axis
    yaxis=dict(gridcolor= colors['chart_gridcolor'])
    )
   
    return  fig, data.to_dict('records')


    

@callback(
    Output('volatility-custom-timeframe', 'children'),
    Input('Stockselection', 'value'),
     Input('Daterange', 'start_date'),
     Input('Daterange', 'end_date'),
     Input('stock-data', 'data')
)
def update_volatility(ticker, start_date, end_date, data_records):

    data = decode_records_data(data_records)
    
    ticker = isin_ticker_to_ticker(ticker)
    vol, num_days = calculate_volatility((start_date, end_date), data, ticker)

    return f'Volatility for the Timeframe from {start_date} to {end_date} ({num_days} trading days) is: {vol:.2f}'








if __name__ == "__main__":
    app.run(debug = True)