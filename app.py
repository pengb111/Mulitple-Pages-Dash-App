import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html,dash_table
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, CSV
from io import StringIO
from page1 import page1
from page2 import page2

app = dash.Dash(external_stylesheets=[dbc.themes.COSMO],
                suppress_callback_exceptions=True)

page1_instance = page1(app)
page2_instance = page2(app)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# sidebar content
sidebar = html.Div(
    [
        html.H2("KDE", className="display-4"),
        html.Hr(),
        html.P(
            "This is used for KDE query display", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Query 1", href="/page-1", active="exact"),
                dbc.NavLink("Query 2", href="/page-2", active="exact"),
                dbc.NavLink("Query 3", href="/page-3", active="exact"),
                dbc.NavLink("Query 4", href="/page-4", active="exact"),
                dbc.NavLink("Query 5", href="/page-5", active="exact"),
                dbc.NavLink("Query 6", href="/page-6", active="exact"),
                dbc.NavLink("Query 7", href="/page-7", active="exact"),
                dbc.NavLink("Query 8", href="/page-8", active="exact"),
                dbc.NavLink("Query 9", href="/page-9", active="exact"),
                dbc.NavLink("Query 10", href="/page-10", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)






content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/page-1":
        return page1_instance.content
    elif pathname == "/page-2":
        return page2_instance.contnet
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


@app.callback(
    Output("query_result", "style_table"), [Input("query_execute", "n_clicks")]
)
# Control the display of the table
def on_button_click(n_clicks):
    if n_clicks is None:
        return {'display': 'none'}
    else:
        return {'display': 'block'}



if __name__ == "__main__":
    app.run_server(debug=True,port=8888)
