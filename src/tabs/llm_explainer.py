#Reuse old parts to save time now:
from dash import html, dcc, Input, Output, callback, ctx
import dash_bootstrap_components as dbc



import dash_bootstrap_components as dbc
import pandas as pd

####
#initial Text
llm_explainer_headline = "LLM Stock movement explanation"
llm_explainer_text = """
Are you unsure about why a Stock moved in a certain direction in a period of time? Do you see large changes in short periods of time you can not explain ?
Use the tools on the bottom left and the plot above to find out why! An LLM will explain why the chosen stock moved that way in the time period chosen in the plot above.
If you are particularly interested in a very specific time period in addition to a larger window, use the configuration below to adjust the explanation to your needs! 

**Disclaimer:** This tool is connected to the Hugging Face API. The models WILL come up with wrong explanations. Use the ´Home` Menu to find out how the backend works and how the prompt is designed. This is ONLY tool only serves a learning purpose and the information is not reliable.
"""

#Define the layout things



llm_explainer_layout = html.Div([
    dbc.Accordion([
        dbc.AccordionItem(
            [
                dcc.Markdown(llm_explainer_text, className='text-center')
            ],
            title=html.Div([
                html.H3(llm_explainer_headline, className='text-center')
            ], style={
                "margin-left": "18rem",
                "padding": "1rem"
            })
        )
    ])
],style={
                "margin-left": "18rem",
                "padding": "1rem"
            })




#html.Br(),
#            dbc.Row(
#                dbc.Col(id='stock_table', width=12))