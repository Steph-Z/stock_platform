import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objects as go

offset_column_1 = 1
offset_column_2 = 4
size_column_1 = 4
size_column_2 = 8

dbc_card = dbc.Card(
    dbc.CardBody(
        dbc.Col(
            [
                dcc.Graph(
                    figure=go.Figure(),
                ),
                dbc.Collapse(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                dbc.Button(
                                    children="Hide",
                                    color="primary",
                                ),
                                html.H5(
                                    children="Hi all",
                                ),
                            ]
                        )
                    ),
                    is_open=True,
                ),
            ]
        ),
    ), className = "mb-4"
)

##### dash app #####

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MINTY],
)

app.layout = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    [
                        dbc.Row(
                            html.Div(
                                dcc.Dropdown(),
                            ),
                            className="mb-3 mx-auto w-75"

                        ),
                        dbc.Row(
                            html.Div(
                                dcc.Dropdown(),
                            ),
                            className="mb-3 mx-auto w-75"
                        ),
                    ],
                ),
                className = "mt-4", # ml-4 doesn't work
                width={"size": size_column_1},
            ),

            dbc.Col(
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc_card,
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc_card,
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc_card,
                                )
                            ]
                        ),
                    ]
                ),
                style={"overflowX":'auto', "overflowY":'auto', 'height':'100%'},
                className = "mt-4 fixed-top",
                width={
                    "size": size_column_2,
                    'offset': f"{offset_column_2}"
                       },
            ),
        ]
    ),
    fluid=True,
)


if __name__ == "__main__":
    app.run(debug=True, port=8000)