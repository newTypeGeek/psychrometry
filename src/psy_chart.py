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

RH_TO_COLOR = {
    10: "rgba(255, 0, 0, 255)",
    20: "rgba(255, 50, 0, 255)",
    30: "rgba(255, 100, 0, 255)",
    40: "rgba(255, 150, 0, 255)",
    50: "rgba(0, 200, 255, 255)",
    60: "rgba(0, 150, 255, 255)",
    70: "rgba(0, 100, 255, 255)",
    80: "rgba(0, 70, 255, 255)",
    90: "rgba(110, 50, 255, 255)",
    100: "rgba(200, 0, 255, 255)",
}


def create_psy_chart() -> go.Figure:
    print("render!")
    fig = go.Figure()

    for rh, humitidy_ratios in RH_TO_HUMIDITY_RATIOS.items():
        # only show lines for every 10% RH
        if rh % 10 == 0:
            line = dict(color=RH_TO_COLOR[rh], width=1)
            showlegend = True
        else:
            line = dict(color="rgba(0,0,0,0)")
            showlegend = False

        rhs = np.array([rh] * NUM_DATA_POINTS)
        customdata = np.stack(
            [
                rhs,
                formula.dew_point_temperature(humitidy_ratios),
                formula.specific_enthalpy(DRY_BULBS, humitidy_ratios),
            ],
            axis=-1,
        )
        hovertemplate = (
            "Dry Bulb: %{x:.1f} °C<br>"
            "Humidity Ratio: %{y:.4f} kg/kg<br>"
            "RH: %{customdata[0]:.1f} %<br>"
            "Dew Point: %{customdata[1]:.1f} °C<br>"
            "Spec. Enthalpy: %{customdata[2]:.1f} kJ/kg"
            "<extra></extra>"
        )
        fig.add_trace(
            go.Scatter(
                x=DRY_BULBS,
                y=humitidy_ratios,
                customdata=customdata,
                showlegend=showlegend,
                line=line,
                name="RH = {:.0f} %".format(rh),
                hovertemplate=hovertemplate,
            )
        )

    fig.update_layout(
        autosize=True,
        height=600,
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
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return fig
