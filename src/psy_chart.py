import enum

import numpy as np
import plotly.graph_objects as go

import formula
import iso_line
import schema

# RH_TO_COLOR = {
#     10: "rgba(255, 0, 0, 255)",
#     20: "rgba(255, 50, 0, 255)",
#     30: "rgba(255, 100, 0, 255)",
#     40: "rgba(255, 150, 0, 255)",
#     50: "rgba(0, 200, 255, 255)",
#     60: "rgba(0, 150, 255, 255)",
#     70: "rgba(0, 100, 255, 255)",
#     80: "rgba(0, 70, 255, 255)",
#     90: "rgba(110, 50, 255, 255)",
#     100: "rgba(200, 0, 255, 255)",
# }


class PsyChart:
    def __init__(self) -> None:
        self._fig = go.Figure()
        self._iso_line = iso_line.IsoLine()

    def render(self) -> go.Figure:
        self._add_iso_lines(
            by=schema.ThermoAttribute.RELATIVE_HUMIDITY, start=1, end=100, step=0.5, iso_display_interval=10
        )
        self._add_iso_lines(by=schema.ThermoAttribute.WET_BULB, start=-12, end=36, step=0.5, iso_display_interval=5)
        self._fig.update_layout(
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

        return self._fig

    def _add_iso_lines(
        self, by: schema.ThermoAttribute, start: int, end: int, step: int, iso_display_interval: int
    ) -> None:
        hovertemplate = (
            "Dry Bulb: %{x:.1f} °C<br>"
            "Humidity Ratio: %{y:.4f} kg/kg<br>"
            "Relative Humidity: %{customdata[0]:.1f} %<br>"
            "Wet Bulb: %{customdata[1]:.1f} °C<br>"
            "Dew Point: %{customdata[2]:.1f} °C<br>"
            "Spec. Enthalpy: %{customdata[3]:.1f} kJ/kg"
            "<extra></extra>"
        )
        for iso_val, attr_to_val in self._iso_line.get_iso_line_thermo_attrs(
            by=by, start=start, end=end, step=step
        ).items():
            # We compute a dense set of points, such that when hovering on the chart, data would be shown
            # Meanwhile, we only show a subset of the iso lines, to avoid cluttering the chart
            if iso_val % iso_display_interval == 0:
                line = dict(color="black", width=1, dash="dash")
                showlegend = True
            else:
                line = dict(color="rgba(0,0,0,0)")
                showlegend = False

            self._fig.add_trace(
                go.Scatter(
                    x=attr_to_val[schema.ThermoAttribute.DRY_BULB],
                    y=attr_to_val[schema.ThermoAttribute.HUMIDITY_RATIO],
                    name="{} = {:.1f}".format(by.name, iso_val),
                    showlegend=showlegend,
                    line=line,
                    customdata=np.stack(
                        [attr_to_val[attr] for attr in schema.ThermoAttribute],
                        axis=-1,
                    ),
                    hovertemplate=hovertemplate,
                )
            )
