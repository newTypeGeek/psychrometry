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

HUMIDITY_RATIO_MAX = 0.03
DRY_BULB_MAX = 50

DRY_BULBS = np.arange(-10, DRY_BULB_MAX, 0.5)

NUM_DATA_POINTS = len(DRY_BULBS)


def generate_humidity_ratios() -> dict[float, np.ndarray]:
    rh_start = 1
    rh_end = 100
    rh_step = 0.5
    rh_to_humidity_ratios = {}
    for rh in np.arange(rh_start, rh_end + rh_step, rh_step):
        humidity_ratios = psy.humidity_ratio(DRY_BULBS, rh)

        rh_to_humidity_ratios[rh] = humidity_ratios

    return rh_to_humidity_ratios


RH_TO_HUMIDITY_RATIOS = generate_humidity_ratios()


@app.callback(Output("graph", "figure"), Input("dropdown", "value"))
def display_color(color):
    print("render!")
    fig = go.Figure()

    for rh, humitidy_ratios in RH_TO_HUMIDITY_RATIOS.items():
        # only show lines for every 10% RH
        if rh % 10 == 0:
            line = None
            showlegend = True
        else:
            line = dict(color="rgba(0,0,0,0)")
            showlegend = False

        fig.add_trace(
            go.Scatter(
                x=DRY_BULBS,
                y=humitidy_ratios,
                customdata=np.stack([[rh] * NUM_DATA_POINTS], axis=-1),
                showlegend=showlegend,
                line=line,
                name="RH = {:.0f} %".format(rh),
                hovertemplate=r"Dry Bulb: %{x:.1f} °C<br>RH: %{customdata[0]:.1f} %<br><extra></extra>",
            )
        )

    fig.update_layout(
        autosize=True,
        height=900,
        # paper_bgcolor="LightSteelBlue",
        title=dict(text=f"Psychrometric Chart (P = {psy.ATMOSPHERIC_PRESSURE} Pa)", font=dict(size=36)),
        yaxis_range=[0, HUMIDITY_RATIO_MAX],
    )

    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
