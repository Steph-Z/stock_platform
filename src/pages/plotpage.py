from dash import html, dcc, Input, Output, callback, State, ctx
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import dash_bootstrap_components as dbc
import pandas as pd
import datetime as dt

from utils.isin_ticker_checkups import check_isin_ticker_input, input_case_insensitive, remove_dashes
from utils.plots import plot_stock_chart
from utils.transforms import decode_records_data, add_currency_information
from utils.config import flatly_colors
from tabs.table_tab import table_layout
from tabs.llm_explainer import llm_explainer_layout

####
#set figures to dark figures
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
#Dexamples in documentations are a lovely thing: https://www.dash-bootstrap-components.com/examples/simple-sidebar/
#https://www.dash-bootstrap-components.com/examples/iris/
#I can sadly not use a sidebar here, since its main purpose is side navigation and not background (input only for one side) things.
#Instead of a Sidebar I can define a column and build the page in a multi columns layout. 

timeframe_buttons = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Button("1M", id="btn-1m", outline=True, className="btn btn-light w-100"), width=4),
                dbc.Col(dbc.Button("3M", id="btn-3m", outline=True, className="btn btn-light w-100"), width=4),
                dbc.Col(dbc.Button("6M", id="btn-6m", outline=True, className="btn btn-light w-100"), width=4),
            ],
            className="mb-2",  #DAMN i just found out about button groups a little later. this would have been need here. Bu ill not reimplement for now :( 
        ),
        dbc.Row(
            [
                dbc.Col(dbc.Button("1Y", id="btn-1y",outline=True, className="btn btn-light w-100"), width=4),
                dbc.Col(dbc.Button("3Y", id="btn-3y",outline=True, className="btn btn-light w-100"), width=4),
                dbc.Col(dbc.Button("5Y", id="btn-5y",outline=True, className="btn btn-light w-100"), width=4),
            ]
        ),
    ]
)


sidebar = html.Div(
    [   html.Br(),
        html.H4("Plot Customization", className="fw-bold"),
        html.Hr(className="my-1"),
        html.Label("Select Timeframe:"),
        timeframe_buttons,
        html.Span('The Plot is interactive! Click and drag your mouse to view a custom window.', className= 'mt-2'),
        html.Span('Double click in the plot to reset it.'),
        html.Hr(className="my-1"),        
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
             style={
                "margin-bottom": "1rem",
                "width": "100%",
                "backgroundColor": flatly_colors["light"], 
                "color": flatly_colors["primary"]
                }
        ),
        html.Hr(className="my-1"),
        html.Label('Y-axis scale:'),
        dbc.RadioItems(['Linear', 'Log'], 'Linear', id = 'axis_scaling', inline= True,
                       labelStyle= {'margin-right': '8px'},
                       style= {'font-size': 14}),
        html.Hr(className="my-1"),
        html.Label("Example Tickers/ ISIN's:", className="mt-3 fw-bold"),
        html.Ul([
            html.Li([html.B("Apple"), ": AAPL or US0378331005"]),
            html.Li([html.B("Microsoft"), ": MSFT or US5949181045"]),
            html.Li([html.B("Nvidia"), ": NVDA or US67066G1040"]),
            html.Li([html.B("AMD"), ": AMD or US0079031078"]),
            html.Li([html.B("SAP"), ": SAP.DE or DE0007164600"]),
            html.Li([html.B("Infineon"), ": IFX.DE or DE0006231004"]),
            html.Li([html.B("ASML"), ": ASML or NL0010273215"])
], style={"fontSize": "14px", "paddingLeft": "1rem"}),
        html.Label('Try to break the input system by using weird spacings or similar. Let me know if I missed something!')
        
        
    ],
    style={
        "color": "white",
        "backgroundColor": flatly_colors["primary"],
        "padding": "1rem",
        "position": "fixed", 
        "top": "85px",  
        "left": 0,
        "bottom": 0,
        "width": "18rem",     
        "overflowY": "auto"
    }
)
#Plot and Table definition:

plot_layout = html.Div(
    [
        html.H4(id='plot_headline'),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id="stocklineplot",
                    figure=go.Figure(layout=go.Layout(template="flatly_dark"))
                ),
                width=12
            )
        )
    ],
    style={
        "margin-left": "18rem"
    }
)

#####Tabs layout 

tabs = dbc.Tabs(
    [
        dbc.Tab(label="Table", tab_id="table"),
        dbc.Tab(label="Metrics", tab_id="metrics"),
        dbc.Tab(label="Ask an LLM", tab_id="llm")
    ],
    id="tabs",
    active_tab="table",
    style={
        "margin-left": "18rem"   # push it to the right of the sidebar
    }
)
###########


# Main page layout now just combines them
layout = dbc.Container([
    dbc.Row([
        sidebar,
        dbc.Col([
            plot_layout,          # plot always visible
            tabs,                 # tabs under the plot
            html.Div(id="tab-content")  # placeholder for tab content
        ])
    ], className="g-0")
], fluid=True,
 style={"overflowX": "hidden", "overflowY": "hidden"})

#Callback to update the plot bassed on the selected stock and data 
@callback(
    Output('stocklineplot', 'figure'),
    Output('plot_headline', 'children'),
    Input('metadata', 'data'),
    Input('axis_scaling', 'value'),
    Input('name_company', 'data'),
    Input('stockdata', 'data'),
    Input('ticker', 'data'),
    Input('chart-type-input', 'value'),
    Input('plot_range', 'data'),
    State('stocklineplot', 'figure')
)

def update_stock_plot(metadata ,axis_type,stock_input_value, stock_data_records,ticker, chart_type, range_dict, figure_old):
    #set date for the figure

    start_date = pd.to_datetime(range_dict['beginning'])
    end_date = pd.to_datetime(range_dict['end'])
    
    # If the figure already has this exact range, skip update
    if figure_old:
        old_range = figure_old.get("layout", {}).get("xaxis", {}).get("range")
        old_chart_type = figure_old.get("layout", {}).get("meta", {}).get("chart_type")
        if old_range:
            old_start, old_end = map(pd.to_datetime, old_range)
            if old_start == start_date and old_end == end_date and old_end == end_date and old_chart_type == chart_type:
                raise PreventUpdate
            
    #empty plot if important data is missing
    if not stock_input_value or not stock_data_records:        
        empty_fig = go.Figure()
        empty_fig.update_xaxes(range= [start_date, end_date])
        
        return empty_fig, f'Interactive plot of the {stock_input_value} stock'
    
    #if we have data decode it and build the figure
    df =decode_records_data(stock_data_records)
    fig = plot_stock_chart(df, comp_name= stock_input_value, ticker= ticker, chart_type= chart_type, metadata= metadata)
    
    
    xaxis_range = [start_date,end_date]
               
    fig.update_xaxes(range=xaxis_range)
    fig.update_layout(meta={"chart_type": chart_type}) #so we store the chart type of a figure to prevent not needed updates
                          
    #fig.update_yaxes(type = axis_type.lower())
    #fig.update_layout(height =  600)

    return fig, f'Interactive plot of the {stock_input_value} stock'


#callback for the button presses
@callback(
    Output('plot_range', 'data',allow_duplicate=True),
    Input("btn-1m", "n_clicks"),
    Input("btn-3m", "n_clicks"),
    Input("btn-6m", "n_clicks"),
    Input("btn-1y", "n_clicks"),
    Input("btn-3y", "n_clicks"),
    Input("btn-5y", "n_clicks"),
    prevent_initial_call=True
)
def update_plot_range_on_button_press(btn1, btn3, btn6, btn1y, btn3y, btn5y):
    
    #to find out which button ws used: https://dash.plotly.com/advanced-callbacks
    #ctx
    #Update the figure if a button is pressed:
    triggered = ctx.triggered_id
    if not triggered:  # nothing pressed
        raise PreventUpdate
    
    end_date = dt.date.today()
    
    if triggered == "btn-1m" and btn1: #This was a big problem: I wanted to store the start and end of the plot, but it was always overwritten by "1 month", 
        #This is because in a dash app, all inputs, even if one spefifies prevent inital call are fired. But the n_clicks changes from None to 0 in that case so the 
        #Initial call has btn value None and not 0. so we need to check both for the button press... ONLY because of the initilization behavior.
        start_date = end_date - pd.DateOffset(months=1)
    elif triggered == "btn-3m" and btn3:
        start_date = end_date - pd.DateOffset(months=3)
    elif triggered == "btn-6m" and btn6:
        start_date = end_date - pd.DateOffset(months=6)
    elif triggered == "btn-1y" and btn1y:
        start_date = end_date - pd.DateOffset(years=1)
    elif triggered == "btn-3y" and btn3y:
        start_date = end_date - pd.DateOffset(years=3)
    elif triggered == "btn-5y" and btn5y:
        start_date = end_date - pd.DateOffset(years=5)
    else:
        #unlikely to encounter, sine it is called by a button press
        start_date = end_date - pd.DateOffset(years=5)
    range_dict = {'beginning': start_date.isoformat(), 'end': end_date.isoformat() }


    return range_dict


@callback(
    Output("plot_range", "data", allow_duplicate=True),
    Input("stocklineplot", "relayoutData"),
    prevent_initial_call=True
)
def update_plot_range_on_mouse(relayout):

    if not relayout:
        raise PreventUpdate

    # relayoutData contains keys like "xaxis.range[0]" and "xaxis.range[1]"
    if "xaxis.range[0]" in relayout and "xaxis.range[1]" in relayout:
        start_date = pd.to_datetime(relayout["xaxis.range[0]"])
        end_date = pd.to_datetime(relayout["xaxis.range[1]"])
        return {"beginning": start_date.isoformat(), "end": end_date.isoformat()}
    
    if "xaxis.autorange" in relayout and relayout["xaxis.autorange"]:

        end_date = pd.Timestamp.today().normalize()
        start_date = end_date - pd.DateOffset(years=5)
        return {"beginning": start_date.isoformat(), "end": end_date.isoformat()}


    #if x axis is not changed 
    raise PreventUpdate

@callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab_content(active_tab):
    if active_tab == "table":
        return table_layout
    elif active_tab == 'metrics':
        return html.Div(dcc.Markdown('Metrics coming soon',style={"margin-left": "18rem","padding": "1rem"}))
    elif active_tab == 'llm':
        return llm_explainer_layout
    return html.Div("No content available.")