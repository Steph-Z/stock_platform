#Reuse old parts to save time now:
#copy paste things from the table tab sincfe this is relly similar
from dash import html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go

import dash_bootstrap_components as dbc
import pandas as pd

from utils.metrics import build_metrics_df
from utils.config import flatly_colors



#general layout of the table tab
metrics_layout = html.Div(
    [   dbc.Row(html.H5(id='metrics_headline', className = 'text-success mb-0',  style={"padding": "0.8rem 1.25rem",   "paddingBottom": "1rem"}), style= {'background': flatly_colors['primary'], 'marginLeft': '1px', 'marginRight': '1px'}),
        html.Br(),
        dbc.Row(
            dbc.Col(id='metrics_table', width=12))
    ],
    style={
        "margin-left": "18rem",
        "padding": "1rem"
    }
)

#Callback for the data in the table
@callback(
    Output('metrics_headline', 'children'),
    Output('metrics_table', 'children'),
    Input('name_company', 'data'), 
    Input('metadata', 'data'), 
       
)
def update_metrics_table(comp_name, metadata):
    if not comp_name:
        return [], []
    
    data = build_metrics_df(metadata)
    table = dbc.Table.from_dataframe(
             data[['Label', 'Value']], striped = True, bordered = False, hover = True
        )
    
    #to make the table scrollable we can put it in another Div container with styling 
    #the styles can be found under: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference, ITs too much for me to really go through
    #all options, so in this case I'll see how it looks and use an LLM to find the styles i need to achieve a specific results
    scrollable_table = html.Div(
        table,
        className= "table-wrapper"
    )

    return f'Detailed information about {comp_name}\'s last 50 trading days',scrollable_table
