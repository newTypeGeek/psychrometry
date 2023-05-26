from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

import psy


app = Dash(__name__)


app.layout = html.Div(
    [
        html.H4("Interactive color selection with simple Dash example"),
        html.P("Select color:"),
        dcc.Dropdown(
            id="dropdown",
            options=["Gold", "MediumTurquoise", "LightGreen"],
            value="Gold",
            clearable=False,
        ),
        dcc.Graph(id="graph"),
    ]
)

HUMIDITY_RATIO_MAX = 0.030
DRY_BULB_MAX = 60

DRY_BULBS = np.arange(-10, DRY_BULB_MAX, 0.5)


def generate_iso_rh_line(rh: float) -> tuple[np.ndarray, np.ndarray]:
    humidity_ratios = psy.humidity_ratio(DRY_BULBS, rh)
    return DRY_BULBS, humidity_ratios


@app.callback(Output("graph", "figure"), Input("dropdown", "value"))
def display_color(color):
    print("render!")
    fig = go.Figure()

    for rh in np.arange(1, 101, 1):
        x, y = generate_iso_rh_line(rh)
        if rh % 10 == 0:  # only show lines for every 10% RH
            fig.add_trace(go.Scatter(x=x, y=y, name=f"RH = {rh} %"))
        else:
            fig.add_trace(go.Scatter(x=x, y=y, showlegend=False, line=dict(color="rgba(0,0,0,0)")))

    fig.update_layout(
        autosize=True,
        height=900,
        # paper_bgcolor="LightSteelBlue",
        title=dict(text="Psychrometric Chart", font=dict(size=48)),
        yaxis_range=[0, HUMIDITY_RATIO_MAX],
    )

    return fig


app.run_server(debug=True)
