#Reuse old parts to save time now:
from dash import html, dcc, Input, Output, callback
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc


from datetime import date, timedelta
import dash_bootstrap_components as dbc
import pandas as pd

from utils.config import flatly_colors

####
#initial Text
llm_explainer_headline = "LLM Stock movement explanation"
llm_explainer_text = """
Are you unsure about why a Stock moved in a certain direction in a period of time? Do you see large changes in short periods of time you can not explain ?
Use the tools on the bottom left and the plot above to find out why! An LLM will explain why the chosen stock moved that way in the time period chosen in the plot above.
If you are particularly interested in a very specific time period in addition to a larger window, use the configuration below to adjust the explanation to your needs! 

**Disclaimer:** This tool is connected to the Hugging Face API. The models WILL come up with wrong explanations.
Use the 'Home' Menu to find out how the backend works and how the prompt is designed.
This tool ONLY serves an educational purpose and the information is not reliable.
"""

#Define the layout things

######Sidebar in the LLM Tab (based on the one defined for the main page)

#Date limits
# Define date limits
today = date.today()
five_years_ago = today - timedelta(days=5*365)

#Sidebar for llm configuration 
sidebar_llm = dbc.Col([
            html.Div([
                html.Div(
                html.H4("LLM Query Setup", className="fw-bold"),
                style={
                    "backgroundColor": flatly_colors['primary'],
                    "color": "white",
                    "borderRadius": "0.5rem",
                    "marginBottom": "1rem"
                }),
                html.Hr(),
                html.Div([
                    dbc.Row([
                    html.Label([
                            "Select Timeframe (updates the plot):"
                        ]),
                    dcc.DatePickerRange(
                        id="llm_main_daterange",
                        min_date_allowed=five_years_ago,
                        max_date_allowed=today,
                        start_date=five_years_ago,
                        display_format="DD.MM.YYYY",
                        end_date=today,
                        style={"margin-bottom": "1rem"}
                    )])]),

                html.Label("Focus on detail period:"),
                dbc.RadioItems(
                    options=[
                        {"label": "Yes", "value": "yes"},
                        {"label": "No", "value": "None"}
                    ],
                    value="None",
                    id="llm_focus_detail",
                    inline=True,
                    labelStyle={"margin-right": "8px"},
                    style={"font-size": 14}
                ),

                html.Div(
                    dcc.DatePickerRange(
                        id="llm_detail_daterange",
                        display_format="DD.MM.YYYY",
                        style={"margin-top": "1rem"}
                    ),
                    id="llm_detail_container"
                ),

                html.Hr(),
                html.Label("Model:"),
                dcc.Dropdown(
                    id="llm_model_dropdown",
                    options=[{"label": "DeepSeek", "value": "deepseek"}],
                    value="deepseek",
                    clearable=False,
                    style={
                        "margin-bottom": "1rem",
                        "width": "100%",
                        "backgroundColor": flatly_colors['light'],
                        "color": flatly_colors['primary']
                    }
                ),

                html.Label("Additional questions:"),
                dcc.Textarea(
                    id="llm_custom_question",
                    placeholder="You have additional questions? Feel free to ask...",
                    disabled=False,
                    style={"width": "100%", "margin-bottom": "1rem", "height": "7rem"}
                ),

                dbc.Button("Get explanation", id="llm_explain_btn", color= 'secondary'),

            ],
            style={
                "color": flatly_colors['light'],
                "backgroundColor": flatly_colors['primary'],
                "padding": "1rem",
                "height": "100%",
                "overflowY": "auto"
            })
        ], width=4)

#llm output window
output_window =  dbc.Col([
            html.Div([
                html.Div(
                html.H4("LLM Output", className="fw-bold"),
                style={
                    "backgroundColor": flatly_colors['primary'],
                    "color": "white",
                    "borderRadius": "0.5rem",
                    "marginBottom": "1rem"
                }
                
                ),
                html.Hr(),
                dbc.Spinner(
                    dcc.Markdown("""Currently, I'm in the process of setting up the Prompt injection as well as the LLM Backend. Thank you for understanding
                                 This Tab has no functionality at the moment while it is being set up 
                                 """, id="llm_output_box"),
                    color= flatly_colors['success']
                )
            ],
            style={
                "color": flatly_colors['light'],
                "backgroundColor": flatly_colors['primary'],
                "padding": "1rem",
                "height": "100%",
                "overflowY": "auto"
            })
        ], width=8)



llm_explainer_layout = html.Div([
    dbc.Accordion([
        dbc.AccordionItem(
            [
                dcc.Markdown(llm_explainer_text, className='text-center')
            ],
            title=html.Div([
                html.H3(llm_explainer_headline, className='text-center')
            ], style={
                "padding": "1rem"
            })
        )
    ]),
    dbc.Row([sidebar_llm,
    output_window])
    
    
    
],style={
                "margin-left": "18rem",
                "padding": "1rem"
            })


###Callback to get the detail daterange

@callback(
    Output("llm_detail_daterange", "disabled"),
    Input("llm_focus_detail", "value")
)
def toggle_detail_enabled(focus_value):
    return focus_value != "yes"
#callback to adjust the plot based on the date picker

@callback(
    Output("llm_main_daterange", "start_date"),
    Output("llm_main_daterange", "end_date"),
    Input("plot_range", "data"),
    prevent_initial_call=True
)
def sync_store_to_datepicker(range_dict):
    if not range_dict:
        raise PreventUpdate
    return range_dict["beginning"], range_dict["end"]

#callback to adjust the datepicker to the range

@callback(
    Output("plot_range", "data", allow_duplicate=True),
    Input("llm_main_daterange", "start_date"),
    Input("llm_main_daterange", "end_date"),
    prevent_initial_call=True
)
def sync_datepicker_to_store(start_date, end_date):
    if not start_date or not end_date:
        raise PreventUpdate
    return {"beginning": pd.to_datetime(start_date).isoformat(),
            "end": pd.to_datetime(end_date).isoformat()}
    
#Updat ethe detail picker based on the range and only allow inputs inside the region:
@callback(
    Output("llm_detail_daterange", "min_date_allowed"),
    Output("llm_detail_daterange", "max_date_allowed"),
    Output("llm_detail_daterange", "start_date"),
    Output("llm_detail_daterange", "end_date"),
    Input("plot_range", "data"),
    prevent_initial_call=True
)
def sync_picker_with_store(range_dict):
    if not range_dict:
        raise PreventUpdate

    start_date = pd.to_datetime(range_dict["beginning"]).date()
    end_date   = pd.to_datetime(range_dict["end"]).date()
    return start_date, end_date, start_date, end_date
