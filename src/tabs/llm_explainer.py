#Reuse old parts to save time now:
from dash import html, dcc, Input, Output, callback, ctx
import dash_bootstrap_components as dbc



import dash_bootstrap_components as dbc
import pandas as pd

####
#initial Text
llm_explainer_text = """
### LLM Stock movement explanation
Are you unsure about why a Stock moved in a certain direction in a period of time? Do you see large changes in short periods of time you can not explain ?
Use the Tools on the left to find out why! 

**Disclaimer:** This tool is connected to the Hugging Face API. The models WILL come up with wrong explanations. Use the ´Home` Menu to find out how the backend works and how the promt is designed. This is ONLY tool only serves a learning purpose and the information is not reliable.


"""

#Define the layout things

llm_explainer_layout = html.Div(
    
        [   dbc.Row(dcc.Markdown(id='llm_explainer_headline_text', llm_explainer_text)),
            
        ],
        style={
            "margin-left": "18rem",
            "padding": "1rem"
        }
    )


#html.Br(),
#            dbc.Row(
#                dbc.Col(id='stock_table', width=12))