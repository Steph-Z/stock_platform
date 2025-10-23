#Reuse old parts to save time now:
from dash import html, dcc, Input, Output, callback, State, no_update
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc


from datetime import date, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import json
from utils.config import flatly_colors



metrics_layout =html.Div(dcc.Markdown('Metrics coming soon',style={"margin-left": "18rem","padding": "1rem"}))