from dash import html, dcc, Input, Output, callback, State, ctx
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

from utils.isin_ticker_checkups import check_isin_ticker_input, input_case_insensitive, remove_dashes
from utils.plots import plot_stock_chart
from utils.misc import colors
from utils.transforms import decode_records_data
from utils.config import pad_for_centering

#Dexamples in documentations are a lovely thing: https://www.dash-bootstrap-components.com/examples/simple-sidebar/
#https://www.dash-bootstrap-components.com/examples/iris/
#I can sadly not use a sidebar here, since its main purpose is side navigation and not background (input only for one side) things.
#Instead of a Sidebar I can define a column and build the page in a multi columns layout. 

timeframe_buttons = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Button("1M", id="btn-1m", outline=True, className="timeframe-btn w-100"), width=4),
                dbc.Col(dbc.Button("3M", id="btn-3m", outline=True, className="timeframe-btn w-100"), width=4),
                dbc.Col(dbc.Button("6M", id="btn-6m", outline=True, className="timeframe-btn w-100"), width=4),
            ],
            className="mb-2",  #DAMN i just found out about button groups a little later. this would have been need here. Bu ill not reimplement for now :( 
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Button("1Y", id="btn-1y",outline=True, className="timeframe-btn w-100"), width=4),
                dbc.Col(dbc.Button("3Y", id="btn-3y",outline=True, className="timeframe-btn w-100"), width=4),
                dbc.Col(dbc.Button("5Y", id="btn-5y",outline=True, className="timeframe-btn w-100"), width=4),
            ]
        ),
    ]
)


sidebar = html.Div(
    [   html.Hr(),
        html.H4("Plot Customization", className="fw-bold"),
        html.Hr(),
        html.Label("Select Timeframe:"),
        timeframe_buttons,
        html.Span('The Plot is inteactive! Click and drag your mouse to view a custom window.'),
        html.Span('Double click in the plot to reset it.'),
        html.Hr(),        
        html.Label("Chart Type:"),
        dcc.Dropdown(
            id="chart-type-input",
            className="plot-dropdown",
            options=[
                {"label": "Line", "value": "line"},
                {"label": "Candlestick", "value": "candlestick"}
            ],
            value="line",
            clearable=False,
            style={"margin-bottom": "1rem", "width": "100%", "textcolor": "black"}
        ),
        html.Hr(),
        html.Label('Y-axis scale:'),
        dcc.RadioItems(['Linear', 'Log'], 'Linear', id = 'axis_scaling', inline= True, labelStyle= {'margin-right': '8px'}, style= {'font-size': 14})
    ],
    style={
        "backgroundColor": "#36536f",
        "color": "white",
        "padding": "1rem",
        "position": "fixed", 
        "top": "80px",  
        "left": 0,
        "bottom": 0,
        "width": "18rem",     
        "overflowY": "auto"
    }
)
#Plot and Table definition:

plot_table = html.Div(
    [   
        html.H4(id ='plot_headline'),
        dbc.Row(
            dbc.Col(dcc.Graph(id="stocklineplot", figure={}), width=10),
            style={"height": "65vh"}
        ),
        html.Hr(),
        html.H4(id ='table_headline'),
        html.Br(),
        dbc.Row(
            dbc.Col(id = 'stock_table', width=10),
            style={"height": "30vh"}
        )
    ],
    style={
        "margin-left": "18rem",  
        "padding": "1rem"
    }
)

layout = dbc.Container([
    dbc.Row([
        sidebar,
        plot_table        
    ], className="g-0")
], fluid=True,
 style= {"overflowX": "hidden",
         "overflowY": "hidden"})

#Callback to update the plot bassed on the selected stock and data 
@callback(
    Output('stocklineplot', 'figure'),
    Output('plot_headline', 'children'),
    Input('axis_scaling', 'value'),
    Input("btn-1m", "n_clicks"),
    Input("btn-3m", "n_clicks"),
    Input("btn-6m", "n_clicks"),
    Input("btn-1y", "n_clicks"),
    Input("btn-3y", "n_clicks"),
    Input("btn-5y", "n_clicks"),
    Input('name_company', 'data'),
    Input('stockdata', 'data'),
    Input('ticker', 'data'),
    Input('chart-type-input', 'value')
)
def update_stock_plot(axis_type, btn1, btn3, btn6, btn1y, btn3y, btn5y, stock_input_value, stock_data_records,ticker, chart_type):
    #to find out which button ws used: https://dash.plotly.com/advanced-callbacks
    #ctx
    if not stock_input_value or not stock_data_records:
        return {}
    
    df =decode_records_data(stock_data_records)
    fig = plot_stock_chart(df, comp_name= stock_input_value, ticker= ticker, chart_type= chart_type)
    
     # Apply consistent color scheme
    fig.update_layout(
        
        template = 'plotly_dark',
        xaxis=dict(gridcolor=colors['chart_gridcolor']),
        yaxis=dict(gridcolor=colors['chart_gridcolor']),
        font_color = colors['text']
    )
    
    #Update the figure if a button is pressed:
    triggered = ctx.triggered_id
    if triggered:
        end_date = df["Date"].max()
        if triggered == "btn-1m":
            start_date = end_date - pd.DateOffset(months=1)
        elif triggered == "btn-3m":
            start_date = end_date - pd.DateOffset(months=3)
        elif triggered == "btn-6m":
            start_date = end_date - pd.DateOffset(months=6)
        elif triggered == "btn-1y":
            start_date = end_date - pd.DateOffset(years=1)
        elif triggered == "btn-3y":
            start_date = end_date - pd.DateOffset(years=3)
        elif triggered == "btn-5y":
            start_date = end_date - pd.DateOffset(years=5)
        else:
            start_date = None

        if start_date is not None:
            xaxis_range = [start_date, end_date]
            #automatically scale Y
            y_min = df.loc[df['Date'].between(start_date, end_date), 'Close'].min()*0.9
            y_max = df.loc[df['Date'].between(start_date, end_date), 'Close'].max()*1.1
            
            fig.update_xaxes(range=xaxis_range)
            if axis_type.lower() == 'linear':
                fig.update_yaxes(range= [y_min, y_max]) 
                          
    fig.update_yaxes(type = axis_type.lower())

    return fig, f'Interactive plot of the {stock_input_value} stock'


#Callback for the data in the table
@callback(
    Output('table_headline', 'children'),
    Output('stock_table', 'children'),
    Input('stockdata', 'data'),
    Input('name_company', 'data'),    
)
def update_stock_table(stock_data, comp_name):
    if not stock_data:
        return [], []
    data = pd.DataFrame(stock_data).sort_index(ascending= False)
    if len(data) > 50:
        data = data.head(50)

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
            "overflowX": "auto",
            "margin": "0 auto",
            "width": "80%",
            "boxShadow": "0px 4px 10px rgba(0,0,0,0.2)",
            "borderRadius": "8px"
        }
    )

    return f'Detailed information about {comp_name}\'s last 50 trading days',scrollable_table