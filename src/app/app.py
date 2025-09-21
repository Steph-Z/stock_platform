from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import yfinance as yf

from pages import landingpage, plotpage

from utils.isin_ticker_checkups import check_isin_ticker_input, input_case_insensitive, remove_dashes
from utils.transforms import isin_ticker_to_ticker, prepare_stock_data


#Initializing the app

#use bootstrap to make it easiert to build a pretty application 
#https://www.dash-bootstrap-components.com/docs/themes/
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions= True)
app.title = 'Stock Dashboard'

#Input section for the stock, shared across different tabs

stock_input = dcc.Input(
        id = 'Stockselection',
        placeholder = "Enter a Ticker or ISIN",
        type = 'text',
        value = 'US0378331005',
        debounce= True,
        style={
        'textAlign': 'center',
        }) 

stock_data_stored = dcc.Store(id = 'stockdata')
comp_name = dcc.Store( id = 'name_company')
ticker = dcc.Store(id= 'ticker')

#Now we build the different Tabs

tabs = dbc.Tabs(
    [
        dbc.Tab(label= 'Home', tab_id= 'home'),
        dbc.Tab(label= 'Charts', tab_id= 'plots')
    ],
    id= 'tabs',
    active_tab= 'home'
)
#We have to define the layout now
#https://www.dash-bootstrap-components.com/docs/quickstart/

explain_text = """This Dashboard is a Work in progress to learn more Software engineering best practices. I test the code, use CI/CD workflows and build a robust 
application. Feel free to pick any Stock you like and explore the tabs. The Github repository can be found under https://github.com/Steph-Z/stock_platform.
\n I hope you enjoy as much as I did building the page."""

app.layout = dbc.Container(
    [
    html.H1("Stock Dashboard", style={'textAlign': 'center'}),
    dcc.Markdown(explain_text),
    stock_input,
    tabs,
    html.Div(id = 'tab-content'),
    stock_data_stored,
    comp_name,
    ticker
    ], #short learning. a Div is a container for almost anything that flows and can be anything
    fluid= True)

#callback to retrieve stock data 
@app.callback(
    Output('stockdata', 'data'),
    Output('name_company', 'data'),
    Output('ticker', 'data'),
    Input('Stockselection', 'value')
)

def retrieve_stock_data(stock_input_value):
    if not stock_input_value:
        return [], None
    
    normed_stock_input =  input_case_insensitive(remove_dashes(stock_input_value))
    ticker = isin_ticker_to_ticker(normed_stock_input) #ToDo more robust
    data = prepare_stock_data(ticker) #To do more robust
    #get the company name for display purposes throuout the app
    comp_name = yf.Ticker(ticker).info['displayName']
    
    return data.to_dict('records'), comp_name,ticker
    
    
    
#Callback to switch tabs
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'active_tab')
)

def render_tab_content(active_tab):
    if active_tab == 'home':
        return landingpage.layout()
    elif active_tab == 'plots':
        return plotpage.layout()
    return 'No Tab selected'


if __name__ == "__main__":
    app.run(debug = True)
 