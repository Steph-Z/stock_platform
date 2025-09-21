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
    Input('name_company', 'data')
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
    
    #to make the table scrollable we can put it in another Div container with styling 
    #the styles can be found under: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference, ITs too much for me to really go through
    #all options, so in this case I'll see how it looks and use an LLM to find the styles i need to achieve a specific results
    scrollable_table = html.Div(
        table,
        style={
            "maxHeight": "400px",
            "overflowY": "auto",
            "margin": "0 auto",
            "width": "80%",
            "boxShadow": "0px 4px 10px rgba(0,0,0,0.2)",
            "borderRadius": "8px"
        }
    )

    return scrollable_table
 
