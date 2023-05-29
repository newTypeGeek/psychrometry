import plotly.graph_objects as go
import numpy as np
import enum

import formula

import iso_line

iso_line_agent = iso_line.IsoLine()

RH_TO_THERMO_PROPERTIES = iso_line_agent.get_iso_line_thermo_attrs(
    by=iso_line.ThermoAttribute.RELATIVE_HUMIDITY, start=1, end=100, step=0.5
)

WET_BULB_TO_THERMO_PROPERTIES = iso_line_agent.get_iso_line_thermo_attrs(
    by=iso_line.ThermoAttribute.WET_BULB, start=-12, end=36, step=0.5
)

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

    for rh, attr_to_vals in RH_TO_THERMO_PROPERTIES.items():
        # only show lines for every 10% RH
        if rh % 10 == 0:
            line = dict(color=RH_TO_COLOR[rh], width=1)
            showlegend = True
        else:
            line = dict(color="rgba(0,0,0,0)")
            showlegend = False

        rhs = np.array([rh] * len(attr_to_vals[iso_line.ThermoAttribute.DRY_BULB]))
        customdata = np.stack(
            [
                rhs,
                attr_to_vals[iso_line.ThermoAttribute.WET_BULB],
                attr_to_vals[iso_line.ThermoAttribute.DEW_POINT],
                attr_to_vals[iso_line.ThermoAttribute.SPECIFIC_ENTHALPY],
            ],
            axis=-1,
        )
        hovertemplate = (
            "Dry Bulb: %{x:.1f} °C<br>"
            "Humidity Ratio: %{y:.4f} kg/kg<br>"
            "Relative Humidity: %{customdata[0]:.1f} %<br>"
            "Wet Bulb: %{customdata[1]:.1f} °C<br>"
            "Dew Point: %{customdata[2]:.1f} °C<br>"
            "Spec. Enthalpy: %{customdata[3]:.1f} kJ/kg"
            "<extra></extra>"
        )
        fig.add_trace(
            go.Scatter(
                x=attr_to_vals[iso_line.ThermoAttribute.DRY_BULB],
                y=attr_to_vals[iso_line.ThermoAttribute.HUMIDITY_RATIO],
                customdata=customdata,
                showlegend=showlegend,
                line=line,
                name="RH = {:.0f} %".format(rh),
                hovertemplate=hovertemplate,
            )
        )

    for wet_bulb, attr_to_vals in WET_BULB_TO_THERMO_PROPERTIES.items():
        # only show lines for every 5°C wet bulb
        if wet_bulb % 5 == 0:
            line = dict(color="black", width=1, dash="dash")
            showlegend = True
        else:
            line = dict(color="rgba(0,0,0,0)")
            showlegend = False

        customdata = np.stack(
            [
                attr_to_vals[iso_line.ThermoAttribute.WET_BULB],
                attr_to_vals[iso_line.ThermoAttribute.RELATIVE_HUMIDITY],
                attr_to_vals[iso_line.ThermoAttribute.DEW_POINT],
                attr_to_vals[iso_line.ThermoAttribute.SPECIFIC_ENTHALPY],
            ],
            axis=-1,
        )
        hovertemplate = (
            "Dry Bulb: %{x:.1f} °C<br>"
            "Humidity Ratio: %{y:.4f} kg/kg<br>"
            "Relative Humidity: %{customdata[1]:.1f} %<br>"
            "Wet Bulb: %{customdata[0]:.1f} °C<br>"
            "Dew Point: %{customdata[2]:.1f} °C<br>"
            "Spec. Enthalpy: %{customdata[3]:.1f} kJ/kg"
            "<extra></extra>"
        )
        fig.add_trace(
            go.Scatter(
                x=attr_to_vals[iso_line.ThermoAttribute.DRY_BULB],
                y=attr_to_vals[iso_line.ThermoAttribute.HUMIDITY_RATIO],
                customdata=customdata,
                showlegend=showlegend,
                line=line,
                name="Wet Bulb = {:.0f}°C".format(wet_bulb),
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
            range=[0, 0.03],
            side="right",
        ),
        legend=dict(
            x=1.1,
            font=dict(size=18),
        ),
        margin=dict(l=0, r=0, t=50, b=0),
    )

    return fig
