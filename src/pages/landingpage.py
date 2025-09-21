from dash import html, dcc, Input, Output, callback

#Define the text on the landing page
landing_text = """Welcome to my landing page"""
def layout():
    
    '''returns the layout of the landing page'''
    
    return html.Div(
        html.H2(landing_text),
        html.Br, #linebreak
        html.Div(id = 'selected_stock_display'),
        style= {'textAlign': 'center'}
    )
    

#Callback to update the stock information, This will ofen be used on all pages
@callback(
    Output('selected_stock_display', 'childen'),
    Input('Stockselection', 'value')
)

def display_selected_stock(stock):
    if stock: 
        return f'Currently the selected stock is: {stock}'
    else:
        return 'Currently no stock is selected'