from dash import dcc, Input, Output, State, ctx
import pandas as pd
import base64
import io
from dash import html
import dash
import dash_bootstrap_components as dbc

# Initialize Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server
