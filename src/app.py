from dash import Dash, dcc, html

import psy_chart

app = Dash(__name__)
app.title = "Psychrometric Chart"

psy_chart_agent = psy_chart.PsyChart()
figure = psy_chart_agent.render()

app.layout = html.Div(
    [
        html.Title("Psychrometric Chart"),
        html.H1("Dash App", style={"textAlign": "center", "color": "black"}),
        dcc.Graph(id="graph", figure=figure),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
