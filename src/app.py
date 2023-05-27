from dash import Dash, dcc, html

import psy_chart


app = Dash(__name__)
app.title = "Psychrometric Chart"


app.layout = html.Div(
    [
        html.Title("Psychrometric Chart"),
        html.H1("Dash App", style={"textAlign": "center", "color": "black"}),
        dcc.Graph(id="graph", figure=psy_chart.create_psy_chart()),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
