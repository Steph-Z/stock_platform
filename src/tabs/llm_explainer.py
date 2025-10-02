#Reuse old parts to save time now:
from dash import html, dcc, Input, Output, callback, State, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc


from datetime import date, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import json
from utils.config import flatly_colors
from utils.transforms import decode_records_data, prepare_data_for_llm
from utils.llm_client import run_deepseek

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
                            "Select Timeframe (updates the plot, Max 3 months for LLM explanation):"
                        ]),
                    dcc.DatePickerRange(
                        id="llm_main_daterange",
                        min_date_allowed=five_years_ago,
                        max_date_allowed=today,
                        start_date= None,
                        display_format="DD.MM.YYYY",
                        end_date= None,
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
                    options=[{"label": "DeepSeek-V3.2", "value": "deepseek"}],
                    value="deepseek",
                    clearable=False,
                    style={
                        "margin-bottom": "1rem",
                        "width": "100%",
                        "backgroundColor": flatly_colors['light'],
                        "color": flatly_colors['primary']
                    }
                ),

                html.Label("Additional questions (max 250 characters):"),
                dcc.Textarea(
                    id="llm_custom_question",
                    placeholder="You have additional questions? Feel free to ask...",
                    disabled=False,
                    maxLength = 250,
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
                    dcc.Markdown("""**Feel free to ask your questions!**
                                 Please keep in mind that hosting an endpoint to an LLM can come with considerable cost. Although I implemented safety measures against high costs. 
                                 This is not a tool to get real financial advise. If you are interested in technical details, I have a thourough explanation (upcoming) in the Home tab. 
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
    html.Div(id="llm_validation_check"), #to throw altert if the input is too long
    dbc.Row([sidebar_llm,
    output_window    
    ])
    
    
    
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

#callback to design the prompt

@callback(
    Output("llm_prompt", "data"),
    Output("llm_validation_check", "children"),
    Input("llm_explain_btn", "n_clicks"),
    State("plot_range", "data"),
    State("stockdata", "data"),
    State("name_company", "data"),
    State("llm_focus_detail", "value"),
    State("llm_detail_daterange", "start_date"),
    State("llm_detail_daterange", "end_date"),
    State("llm_custom_question", "value"),
    State("llm_model_dropdown", "value"),
    prevent_initial_call=True
)
def prompt_injection(button_fire, plot_range, data, comp_name, focus_setting, focus_range_start, focus_range_end, extra_questions, model_type):
    '''the prompt injection using the dynamic/changing  variables to design the prompt for the llm analysis'''
    if not button_fire:  #stops the inital call, as n_clicks is  None is first call/inital one 
        raise PreventUpdate
    start_date = pd.to_datetime(plot_range['beginning'])
    end_date = pd.to_datetime(plot_range['end'])
    #check if range is not larger than 3 months:
    #this is to avoid long input tokens
    if (end_date- start_date).days > 100: #generous impl :) 
        return None, dbc.Alert("Please select a maximum range of 3 months for analysis.",color="danger",
            dismissable=True,
            is_open=True
        )
    df =decode_records_data(data)
    df = df.loc[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    df = prepare_data_for_llm(df)
    
    if focus_setting == 'yes':
        focus_string = f'The user also wants you to pay special attention to this interval {focus_range_start}, {focus_range_end}'
    else:
        focus_string = ''
    
    #catch an empty box, do in two steps to evaluate, for robust prompt building 
    try:
        if extra_questions.strip() == '':
            extra_questions = None
    except Exception:
        pass
    if extra_questions != None:
        extra_tasks = f"The user also has additional questions which you should answer only if they are related to the stock input. Here is the user's input: {json.dumps(extra_questions)}"
    else:
        extra_tasks = ''
        
        

    prompt = f'''Your role is a stock analyst for a financial dashboard.
    The user of the dashboard wants to know why the stock of a company moved the way it did.
    You provide a short, about 200 words long analysis not matter what the users states.
    Your output will be rendered in a Markdown menu, so use markdown formatting for a short but coherent analysis.
    Start the output with ### Analysis of {comp_name}.
    The name of the Company is {comp_name}. Focus on the time period present in the data and explain why the stock moved the way it did.
    The data shows the days and how much (in %) the stock moved. {df}
    {focus_string}, {extra_tasks}    
    '''
    return prompt, None


@callback(
    Output("llm_output_box", "children"),
    Input("llm_prompt", "data"),
    prevent_initial_call=True
)
def call_llm(prompt):
    #output = '### Analysis of Tesla'
    output = run_deepseek(prompt, max_tokens = 500)
    return output