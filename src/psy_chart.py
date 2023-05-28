import plotly.graph_objects as go
import numpy as np
import enum

import formula

HUMIDITY_RATIO_MAX = 0.03
DRY_BULB_MAX = 50

DRY_BULBS = np.arange(-10, DRY_BULB_MAX, 0.5)

NUM_DATA_POINTS = len(DRY_BULBS)


class ThermoProperty(enum.Enum):
    RELATIVE_HUMIDITY = "relative_humidity"
    HUMIDITY_RATIO = "humidity_ratio"
    WET_BULB = "wet_bulb"
    DEW_POINT = "dew_point"
    SPECIFIC_ENTHALPY = "specific_enthalpy"


def precompute_thermo_properties_by_rh() -> dict[float, dict[ThermoProperty, np.ndarray]]:
    rh_start = 1
    rh_end = 100
    rh_step = 0.5
    rh_to_thermo_properties = {}
    for rh in np.arange(rh_start, rh_end + rh_step, rh_step):
        humidity_ratios = formula.humidity_ratio(DRY_BULBS, rh)
        rh_to_thermo_properties[rh] = {}
        rh_to_thermo_properties[rh][ThermoProperty.HUMIDITY_RATIO] = humidity_ratios
        rh_to_thermo_properties[rh][ThermoProperty.WET_BULB] = formula.wet_bulb_temperature(DRY_BULBS, rh)
        rh_to_thermo_properties[rh][ThermoProperty.DEW_POINT] = formula.dew_point_temperature(humidity_ratios)
        rh_to_thermo_properties[rh][ThermoProperty.SPECIFIC_ENTHALPY] = formula.specific_enthalpy(
            DRY_BULBS, humidity_ratios
        )

    return rh_to_thermo_properties


def precompute_thermo_properties_by_wet_bulb() -> dict[float, dict[ThermoProperty, np.ndarray]]:
    wet_bulb_start = -12
    wet_bulb_end = 36
    wet_bulb_step = 0.5
    wet_bulb_to_themo_properties = {}
    for wet_bulb in np.arange(wet_bulb_start, wet_bulb_end + wet_bulb_step, wet_bulb_step):
        humidity_ratios = formula.humidity_ratio_by_dry_bulb_and_wet_bulb(DRY_BULBS, wet_bulb)
        wet_bulb_to_themo_properties[wet_bulb] = {}
        wet_bulb_to_themo_properties[wet_bulb][ThermoProperty.HUMIDITY_RATIO] = humidity_ratios
        wet_bulb_to_themo_properties[wet_bulb][ThermoProperty.RELATIVE_HUMIDITY] = formula.relative_humidity(
            DRY_BULBS, humidity_ratios
        )
        wet_bulb_to_themo_properties[wet_bulb][ThermoProperty.DEW_POINT] = formula.dew_point_temperature(
            humidity_ratios
        )
        wet_bulb_to_themo_properties[wet_bulb][ThermoProperty.SPECIFIC_ENTHALPY] = formula.specific_enthalpy(
            DRY_BULBS, humidity_ratios
        )
    return wet_bulb_to_themo_properties


RH_TO_THERMO_PROPERTIES = precompute_thermo_properties_by_rh()

WET_BULB_TO_THERMO_PROPERTIES = precompute_thermo_properties_by_wet_bulb()

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

        rhs = np.array([rh] * NUM_DATA_POINTS)
        customdata = np.stack(
            [
                rhs,
                attr_to_vals[ThermoProperty.WET_BULB],
                attr_to_vals[ThermoProperty.DEW_POINT],
                attr_to_vals[ThermoProperty.SPECIFIC_ENTHALPY],
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
                x=DRY_BULBS,
                y=attr_to_vals[ThermoProperty.HUMIDITY_RATIO],
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

        wet_bulbs = np.array([wet_bulb] * NUM_DATA_POINTS)
        customdata = np.stack(
            [
                wet_bulbs,
                attr_to_vals[ThermoProperty.RELATIVE_HUMIDITY],
                attr_to_vals[ThermoProperty.DEW_POINT],
                attr_to_vals[ThermoProperty.SPECIFIC_ENTHALPY],
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
                x=DRY_BULBS,
                y=attr_to_vals[ThermoProperty.HUMIDITY_RATIO],
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
