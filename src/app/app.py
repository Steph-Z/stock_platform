import yfinance as yf
import pandas as pd
import plotly.express as px 
from dash import Dash, dcc, html, Input, Output, callback

from utils.metrics import calculate_volatility
from utils.plots import plot_stock_chart_line
from utils.transforms import isin_ticker_to_ticker

#Initializing the app

app = Dash()
app.title = "Stock Dashboard"

#########Color settings

colors = {    'background': '#111111',
        'input_background': "#7572728A",
        'text': '#7FDBFF'
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
        value = 'AAPL',
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
        end_date = '2025-09-01'),
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
        
    data = yf.download(f'{ticker}', period = 'max')
    data.columns = data.columns.get_level_values(0) #get rid of the multi index for easier cashing
    data = data.reset_index()
    data.index.name = 'Date'
    #get the figure 
    fig = plot_stock_chart_line(data = data, ticker = ticker)
    #change colors of the figure to match the layout
    fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
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

    data = pd.DataFrame(data_records)
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.set_index("Date")
    data.index.name = 'Date'
    
    ticker = isin_ticker_to_ticker(ticker)
    vol, num_days = calculate_volatility((start_date, end_date), data, ticker)

    return f'Volatility for the Timeframe from {start_date} to {end_date} ({num_days} trading days) is: {vol:.2f}'






if __name__ == "__main__":
    app.run(debug = True)