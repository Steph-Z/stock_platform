from dash import Dash, dcc, html, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import yfinance as yf
import plotly.graph_objects as go
import plotly.io as pio
import logging
import pandas as pd
#adding a cash



from utils.isin_ticker_checkups import check_isin_ticker_input, input_case_insensitive, remove_dashes
from utils.transforms import isin_ticker_to_ticker, prepare_stock_data, get_stock_metadata, clean_comp_name

from utils.config import flatly_colors

#Import of the LAyouts of other sides 
from pages.home import layout as  home_layout
from pages.plotpage import layout as chart_layout

###############Logging for debugging#########

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
#logger = logging.getLogger(__name__)

################################################
#Initializing the app
#setting the colors for figures to have coherent look
flatly_dark_template = go.layout.Template(
    layout=go.Layout(
        paper_bgcolor=flatly_colors["background"],
        plot_bgcolor=flatly_colors["background"],
        font=dict(color=flatly_colors["light"]),
        xaxis=dict(showgrid=True, gridcolor=flatly_colors["secondary"]),
        yaxis=dict(showgrid=True, gridcolor=flatly_colors["secondary"])
    )
)

# Register and set as default
pio.templates["flatly_dark"] = flatly_dark_template
pio.templates.default = "flatly_dark"


#use bootstrap to make it easiert to build a pretty application 
#https://www.dash-bootstrap-components.com/docs/themes/

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY],  suppress_callback_exceptions= True)
app.title = 'Stock Dashboard'
#To host the app
server = app.server

################################################
#Navbar Definition
#Input section for the stock, shared across different sides of the navbar
#Input now treated like a search box : https://www.dash-bootstrap-components.com/docs/components/navbar/#
#good explanation for the col solution here: https://www.dash-bootstrap-components.com/docs/components/layout/

#Title/Nav Text
perma_text = 'Plotpoint'
perma_subtext ='by Steph'


#Stock input 
stock_input = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Span('Enter ISIN/Ticker:', style={'color': 'white', 'marginRight': '10px'}),
                    width='auto'
                ),
                dbc.Col(
                    dbc.Input(
                        id='Stockselection',
                        type='text',
                        placeholder='ISIN/Ticker',
                        value='US0378331005',
                        size='sm',
                        debounce = True,
                        class_name= ('bg-light text-dark')
                    ),
                    width='auto',
                ),
                dbc.Col(
                    dbc.Button('Enter', id='stockbutton', color='secondary', size='sm', className='ms-auto'),
                    width='auto',
                ),
            ],
            align='center',
            className='g-2',
        ),

        dbc.Row(
            dbc.Col(
                html.Span(id='current_stock', style={'color': 'white'}),
                width='auto'  
            ),
            className='mt-2' 
        )
    ]
)

#Navbar
page_links = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink('Home', href='/', active='exact')),
        dbc.NavItem(dbc.NavLink('Dashboard', href='/dashboard', active='exact')),
    ],
    pills=True,
    navbar=True,
    className='ms-2'
)

navbar = dbc.Navbar(
    dbc.Container(
        dbc.Row([
            dbc.Col(page_links, width='auto', className='d-flex align-items-center'),
            dbc.Col(
            html.Div([
                html.H2(perma_text, style={'color': 'white', 'marginRight': '10px'}),
                html.H6(perma_subtext, style={'color': 'lightgray', 'marginTop': '8px'})
            ],
            style={'display': 'flex', 'alignItems': 'flex-end'}),
            className='d-flex justify-content-center',
            width=True
        ),
            dbc.Col(stock_input, width='auto', className='d-flex align-items-center'),
        ],
        align='center',
        className='w-100 g-2'),
        fluid=True
    ),
    color='primary',
    dark=True,
    sticky='top'
)
 
################################################################################################
#Caches for easy access in different tabs and places on the navbar, these need to be shared across the different navbar sides

global_stores = html.Div(
    [
    dcc.Store(id = 'stockdata'),
    dcc.Store( id = 'name_company'), #altough in metadata, depending on where the company is from its a different name [name_long],
    #[name_short], sot this is easier to sore like that
    dcc.Store(id= 'ticker'),
    dcc.Store(id= 'metadata')
    ]    
)

################################################################################################
#Layout of hte main app
#https://www.dash-bootstrap-components.com/docs/quickstart/

app.layout = html.Div(
    [
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', style={"padding": "20px"}),
    global_stores
    ])

#Collapsing the navbar
@app.callback(Output("navbarcollapse", "is_open"),
              Input("navbar-toggler", "n_clicks"),
              State("navbarcollapse", "is_open")
)

def toggle_navbar(n, is_open):
    if n:
        return not is_open
    return is_open

#callback to get the right page
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))

def display_page(path):
    if path == '/dashboard':
        return chart_layout
    else:
        return home_layout

#callback to retrieve stock data based on the userinput
@app.callback(
    Output('stockdata', 'data'),
    Output('name_company', 'data'),
    Output('ticker', 'data'),
    Output('current_stock', 'children'),
    Output('metadata', 'data'),
    Input('stockbutton', 'n_clicks'),
    Input('Stockselection', 'value',)
)

def retrieve_stock_data( n_clicks, stock_input_value):
    if not stock_input_value:
        return [], None, None, 'Invalid, No Input detected'

    try:    
        normed_stock_input =  input_case_insensitive(remove_dashes(stock_input_value))
        ticker = isin_ticker_to_ticker(normed_stock_input) #ToDo more robust
        data = prepare_stock_data(ticker) #To do more robust, data is in json format here 
        metadata = get_stock_metadata(ticker)
        
        if data.empty:            
            return [], None, None, f'Input: {normed_stock_input} exists, but no data is available', None
        #get the company name for display purposes throuout the app
        #PROBLEM: some international tickers do not have the displayNAme (like adidas) so we need something more robust here 
        comp_name = comp_name = metadata.get('shortName') or metadata.get('displayName') or metadata.get('longName') or ticker
        #Problem: international stocks like i.e infineon are poorly documented and or have their Stock type in the company name this 
        #will lead to trailing letters in this case 'INFINEON TECHNOLOGIES AG      N' 
        #So to make the company name as pretty as possible we have to find anre remove trailin letters ad numbers
        comp_name = clean_comp_name(comp_name)
        return data.to_dict('records'), comp_name, ticker, f'Company Name: {comp_name}', metadata
    except Exception:
        return [], None, None, f'Invalid: {normed_stock_input} is not a valid ticker or ISIN', None
    
    
    


#not needed anymore since I introcuded a main.py as a convinient entry point
##general rule; here we run in debug = True, in main we do not
if __name__ == "__main__":
    app.run(debug = True)
    
    





 