from dash import html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go


import dash_bootstrap_components as dbc
import pandas as pd

from utils.transforms import decode_records_data, add_currency_information
from utils.config import flatly_colors



#general layout of the table tab
table_layout = html.Div(
    [   dbc.Row(html.H5(id='table_headline', className = 'text-success mb-0',  style={"padding": "0.8rem 1.25rem",   "paddingBottom": "1rem"}), style= {'background': flatly_colors['primary'], 'marginLeft': '1px', 'marginRight': '1px'}),
        html.Br(),
        dbc.Row(
            dbc.Col(id='stock_table', width=12))
    ],
    style={
        "margin-left": "18rem",
        "padding": "1rem"
    }
)

#Callback for the data in the table
@callback(
    Output('table_headline', 'children'),
    Output('stock_table', 'children'),
    Input('stockdata', 'data'),
    Input('name_company', 'data'), 
    Input('metadata', 'data'), 
       
)
def update_stock_table(stock_data, comp_name, metadata):
    if not stock_data:
        return [], []
    stock_data =decode_records_data(stock_data)
    data = pd.DataFrame(stock_data).sort_index(ascending= False)
    if len(data) > 50:
        data = data.head(50)

    data["Date"] = pd.to_datetime(data["Date"]).dt.strftime("%d.%m.%Y") 
    #example of llm usage for data wrangling
    data = data.assign(**{col: data[col].map(lambda x: add_currency_information(x, metadata["currency"])) for col in ["Open", "High", "Low", "Close"]},Volume=data["Volume"].map(lambda x: f"{x:,.0f}")
)
    table = dbc.Table.from_dataframe(
             data, striped = True, bordered = False, hover = True
        )
    
    #to make the table scrollable we can put it in another Div container with styling 
    #the styles can be found under: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference, ITs too much for me to really go through
    #all options, so in this case I'll see how it looks and use an LLM to find the styles i need to achieve a specific results
    scrollable_table = html.Div(
        table,
        className= "table-wrapper"
    )

    return f'Detailed information about {comp_name}\'s last 50 trading days',scrollable_table