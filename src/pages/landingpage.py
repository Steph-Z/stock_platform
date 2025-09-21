from dash import html, dcc, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd


#Define the text on the landing page
landing_text = """Welcome to my landing page"""
def layout():
    
    '''returns the layout of the landing page'''
    
    return html.Div(
        [
        html.H2(landing_text),
        html.Br(), #linebreak
        html.Div(id = 'selected_stock_display'),        
        html.Div(id = 'stock_table'),
        ],
        style= {'textAlign': 'center'}
    )
    

#Callback to update the stock information, This will ofen be used on all pages
@callback(
    Output('selected_stock_display', 'children'),
    Input('Stockselection', 'value')
)

def display_selected_stock(stock):
    if stock: 
        return f'Currently the selected stock is: {stock}'
    else:
        return 'Currently no stock is selected'
    
#Callback for the data in the table
@callback(
    Output('stock_table', 'children'),
    Input('stockdata', 'data')
)
def update_stock_table(stock_data):
    if not stock_data:
        return [], []
    data = pd.DataFrame(stock_data).sort_index(ascending= False)
    if len(data) > 100:

        data = data.head(100)
        data["Date"] = pd.to_datetime(data["Date"]).dt.strftime("%d.%m.%Y") 
        table = dbc.Table.from_dataframe(
             data.round(2), striped=True, bordered=True, hover=True, index=False, responsive = True
        )

        return table
    else:
        table = dbc.Table.from_dataframe(
             data.round(2), striped=True, bordered=True, hover=True, index= False, responsive = True
        )
        return table
        