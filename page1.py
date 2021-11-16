import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html, dash_table, State
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, CSV
from io import StringIO

# Get the query results
# Connect to the data
sparql = SPARQLWrapper("http://localhost:7200/repositories/test")

# Set query code
sparql.setQuery("""
PREFIX ex: <http://example.org/>
SELECT ?station ?HeightValue
WHERE {
?station ex:Height ?HeightValue .
}
ORDER BY ASC(?HeightValue)
LIMIT 20
""")
# Get the data and change the format
sparql.setReturnFormat(CSV)
results = sparql.query().convert().decode("utf-8")
results = StringIO(results)
df = pd.read_csv(results)
df.insert(loc=0, column='#', value=df.index)

radioitems1 = html.Div(
    [
        dbc.Label(html.H3("Education Level")),
        dbc.RadioItems(
            options=[
                {"label": "Primary", "value": 1},
                {"label": "Lower secondary", "value": 2},
                {"label": "Upper secondary", "value": 3},
                {"label": "Post leaving cert", "value": 4},
                {"label": "Third level", "value": 5},
                {"label": "Higher certificate", "value": 6},
                {"label": "Ordinary bachelor degree/professional qualification or both", "value": 7},
                {"label": "Honours bachelor degree/professional qualification or both", "value": 8},
                {"label": "Postgraduate diploma/degree or Doctorate (Ph.D.)", "value": 9},
            ],
            value=1,
            id="radioitems-input1",
            inline=True
        ),
    ]
)

eductionLevel_RI = {
    1:"Primary",
    2:"Lower secondary",
    3:"Upper secondary",
    4:"Post leaving cert",
    5:"Third level",
    6:"Higher certificate",
    7:"Ordinary bachelor degree/professional qualification or both",
    8:"Honours bachelor degree/professional qualification or both",
    9:"Postgraduate diploma/degree or Doctorate (Ph.D.)"
}

radioitems2 = html.Div(
    [
        dbc.Label(html.H3("Region")),
        dbc.RadioItems(
            options=[
                {"label": "State", "value": 1},
                {"label": "Border", "value": 2},
                {"label": "Midland", "value": 3},
                {"label": "West", "value": 4},
                {"label": "Dublin", "value": 5},
                {"label": "Mid-East", "value": 6},
                {"label": "South-East", "value": 7},
                {"label": "South-West", "value": 8},

            ],
            value=1,
            id="radioitems-input2",
            inline=True
        ),
    ]
)

radioitems3 = html.Div(
    [
        dbc.Label(html.H3("Year")),
        dbc.RadioItems(
            options=[
                {"label": "2009Q2", "value": 1},
                {"label": "2010Q2", "value": 2},
                {"label": "2011Q2", "value": 3},
                {"label": "2012Q2", "value": 4},
                {"label": "2013Q2", "value": 5},
                {"label": "2014Q2", "value": 6},
                {"label": "2015Q2", "value": 7},
                {"label": "2016Q2", "value": 8},
                {"label": "2017Q2", "value": 9},
                {"label": "2018Q2", "value": 10},
                {"label": "2019Q2", "value": 11},
                {"label": "2020Q2", "value": 12},

            ],
            value=1,
            id="radioitems-input3",
            inline=True
        ),
    ]
)

page_1 = html.Div([
    dbc.Container(
        [
            # Get the first parameter
            radioitems1,
            html.Br(),
            radioitems2,
            html.Div(id="radioitems-checklist-output"),
            html.Br(),
            radioitems3,
            html.Br(),
            dbc.InputGroup(
            [dbc.InputGroupText("Limit"), dbc.Input(placeholder="Limit Number of the showed data no more than 1000",
                                                    id="limit_number",
                                                    type="number", min=0, max=1000,value=20,)],
            className="mb-3",
            ),
            dbc.Button("Query", color='primary', id="query_btn"),
            html.Br(),
            html.H2("Result"),
            html.Div( id="rst_container",
                children= dash_table.DataTable(
                id="query_result",
                columns=[{'name': column, 'id': column} for column in df.columns],
                data=df.to_dict('records'),
                virtualization=True,
                style_table={
                    'height': '300px',
                    'display': 'block',
                },
                fixed_rows={'headers': True},
                style_header={
                    'background-color': '#b3e5fc',
                    'font-family': 'Times New Roman',
                    'font-weight': 'bold',
                    'font-size': '17px',
                    'text-align': 'left',

                },
                style_data={
                    'font-family': 'Times New Roman',
                    'text-align': 'left'
                },
                style_cell_conditional=[
                    {'if': {'column_id': '#'},
                     'width': '10%'},
                    {'if': {'column_id': 'station'},
                     'width': '50%'},
                    {'if': {'column_id': 'HeightValue'},
                     'width': '40%'},
                ],
            )
            ),
            html.Br(),

        ],

    ),

]
)

def on_form_change(nclicked,eduLevel,region,year,limit):
    if nclicked is not None:
        print(nclicked,eductionLevel_RI[eduLevel],region,year,limit)
        # 在此处构造查询语句
        # 例如 （以limit 为例）
        sparql.setQuery(f""" 
        PREFIX ex: <http://example.org/>
        SELECT ?station ?HeightValue
        WHERE {{
        ?station ex:Height ?HeightValue .
        }}
        ORDER BY ASC(?HeightValue)
        LIMIT {limit}
        """)
        # 查询
        sparql.setReturnFormat(CSV)
        results = sparql.query().convert().decode("utf-8")
        results = StringIO(results)
        df = pd.read_csv(results)
        df.insert(loc=0, column='#', value=df.index)
        return dash_table.DataTable(
                    id="query_result",
                    columns=[{'name': column, 'id': column} for column in df.columns],
                    data=df.to_dict('records'),
                    virtualization=True,
                    style_table={
                        'height': '300px',
                        'display': 'block',
                    },
                    fixed_rows={'headers': True},
                    style_header={
                        'background-color': '#b3e5fc',
                        'font-family': 'Times New Roman',
                        'font-weight': 'bold',
                        'font-size': '17px',
                        'text-align': 'left',

                    },
                    style_data={
                        'font-family': 'Times New Roman',
                        'text-align': 'left'
                    },
                    style_cell_conditional=[
                        {'if': {'column_id': '#'},
                         'width': '10%'},
                        {'if': {'column_id': 'station'},
                         'width': '50%'},
                        {'if': {'column_id': 'HeightValue'},
                         'width': '40%'},
                    ],
                )

# @app.callback(Output(),[Input()...],[State()])
# def handleNewQuery(){
#
# }

class page1:
    def __init__(self, app):
        self.content = page_1
        app.callback(Output("rst_container", "children"),[Input("query_btn","n_clicks")],
    [
        State("radioitems-input1", "value"),
        State("radioitems-input2", "value"),
        State("radioitems-input3", "value"),
        State("limit_number", "value")
    ])(on_form_change)

