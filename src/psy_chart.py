import plotly.graph_objects as go
import numpy as np

import formula

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
        humidity_ratios = formula.humidity_ratio(DRY_BULBS, rh)

        rh_to_humidity_ratios[rh] = humidity_ratios

    return rh_to_humidity_ratios


RH_TO_HUMIDITY_RATIOS = generate_humidity_ratios()


def create_psy_chart() -> go.Figure:
    print("render!")
    fig = go.Figure()

    for rh, humitidy_ratios in RH_TO_HUMIDITY_RATIOS.items():
        # only show lines for every 10% RH
        if rh % 10 == 0:
            line = dict(color="blueviolet")
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
        # height=900,
        # paper_bgcolor="LightSteelBlue",
        title=dict(text=f"Psychrometric Chart (P = {formula.ATMOSPHERIC_PRESSURE} Pa)", font=dict(size=22)),
        xaxis=dict(
            title=dict(text="Dry Bulb Temperature (°C)", font=dict(size=18)),
        ),
        yaxis=dict(
            title=dict(text="Humidity Ratio (kg/kg)", font=dict(size=18)),
            range=[0, HUMIDITY_RATIO_MAX],
            side="right",
        ),
        legend=dict(
            x=1.1,
            font=dict(size=18),
        ),
    )

    return fig
