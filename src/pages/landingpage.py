from dash import html, dcc, Input, Output, callback, dash_table
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
        dash_table.DataTable( #https://dash.plotly.com/datatable/height need to be careful with the displaying of large tables 
            id = 'stock_table',
            data = [],
            columns = [],
            page_size=30,  
            style_table={'height': '400px', 'overflowY': 'auto'}
        ),
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
    Output('stock_table', 'data'),
    Output('stock_table', 'columns'),
    Input('stockdata', 'data')
)
def update_stock_table(stock_data):
    if not stock_data:
        return [], []
    
    columns = [{'name': col, 'id': col} for col in stock_data[0].keys()]
    if len(pd.DataFrame(stock_data)) > 50:
        return pd.DataFrame(stock_data).head(50).to_dict('records'), columns
    else:
        return stock_data, columns
        