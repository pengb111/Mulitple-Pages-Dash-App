import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, dash_table, State
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, CSV
from io import StringIO

content = html.Div(children=[html.H1("",id="content-div"),
                             html.Button("Hello",id="hello_btn")])

def handleBtn(nclicks):
    if nclicks is not None:
        return "Pengbo is the best!"

class page2:
    def __init__(self,app):
        self.contnet = content
        app.callback(Output("content-div","children"),[Input("hello_btn","n_clicks")])(handleBtn)