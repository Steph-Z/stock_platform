from dash import Dash, dcc, html, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import yfinance as yf

from utils.isin_ticker_checkups import check_isin_ticker_input, input_case_insensitive, remove_dashes
from utils.transforms import isin_ticker_to_ticker, prepare_stock_data

#Import of the LAyouts of other sides 
from pages.home import layout as  home_layout
from pages.plotpage import layout as chart_layout


################################################
#Initializing the app


#use bootstrap to make it easiert to build a pretty application 
#https://www.dash-bootstrap-components.com/docs/themes/

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],  suppress_callback_exceptions= True)
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
                    ),
                    width='auto',
                ),
                dbc.Col(
                    dbc.Button('Enter', id='stockbutton', color='primary', size='sm', className='ms-auto'),
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
        dbc.NavItem(dbc.NavLink('Plots/Tables', href='/charts', active='exact')),
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
    color='dark',
    dark=True,
    sticky='top'
)
 
################################################################################################
#Caches for easy access in different tabs and places on the navbar, these need to be shared across the different navbar sides

global_stores = html.Div(
    [
    dcc.Store(id = 'stockdata'),
    dcc.Store( id = 'name_company'),
    dcc.Store(id= 'ticker')
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
    if path == '/charts':
        return chart_layout
    else:
        return home_layout

#callback to retrieve stock data based on the userinput
@app.callback(
    Output('stockdata', 'data'),
    Output('name_company', 'data'),
    Output('ticker', 'data'),
    Output('current_stock', 'children'),
    State('Stockselection', 'value',),
    Input('stockbutton', 'n_clicks')
)

def retrieve_stock_data(stock_input_value, n_clicks):
    if not stock_input_value:
        return [], None, None, 'Invalid'

    try:    
        normed_stock_input =  input_case_insensitive(remove_dashes(stock_input_value))
        ticker = isin_ticker_to_ticker(normed_stock_input) #ToDo more robust
        data = prepare_stock_data(ticker) #To do more robust
        #get the company name for display purposes throuout the app
        comp_name = yf.Ticker(ticker).info['displayName']
        
        return data.to_dict('records'), comp_name,ticker, f'Company Name: {comp_name}'
    except Exception:
        return [], None, None, 'Invalid'
    
    
    


#not needed anymore since I introcuded a main.py as a convinient entry point
##general rule; here we run in debug = True, in main we do not
if __name__ == "__main__":
    app.run(debug = True)
    
    





 