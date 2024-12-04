import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
from heatmap import get_heatmap_layout, register_heatmap_callbacks
from line_chart import get_line_chart_layout, register_line_chart_callbacks
from choropleth import get_choropleth_layout, register_choropleth_callbacks
from predictive_modeling import get_predictive_modeling_layout, register_predictive_modeling_callbacks

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Suppress callback exceptions for dynamic layouts
app.config.suppress_callback_exceptions = True

# Define the main layout
app.layout = dbc.Container([
    html.H1("Global Climate Dashboard"),

    html.Div([
        html.H2("Select a Feature:"),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id="feature-selector",
                    options=[
                        {"label": "Heatmap", "value": "heatmap"},
                        {"label": "Line Chart", "value": "line_chart"},
                        {"label": "Choropleth Map", "value": "choropleth"},
                        {"label": "Predictive Modeling", "value": "predictive_modeling"},  # New option
                    ],
                    value="heatmap",
                    clearable=False,
                    style={"width": "100%"}
                ),
                width=12,
            )
        ])
    ], style={"marginBottom": "20px"}),

    html.Div(id="feature-content"),
], fluid=True)



# Callback to dynamically load content based on selected feature
@app.callback(
    Output("feature-content", "children"),
    [Input("feature-selector", "value")]
)
def display_feature(feature):
    if feature == "heatmap":
        return get_heatmap_layout()  # load heatmap layout
    elif feature == "line_chart":
        return get_line_chart_layout()  # Load line chart layout
    elif feature == "choropleth":
        return get_choropleth_layout()  # Load choropleth map layout
    elif feature == "predictive_modeling":
        return get_predictive_modeling_layout()  # Load predictive modeling layout
    # Add more conditions for other features
    return html.Div("Select a valid feature.")


# Register callbacks for each feature
register_heatmap_callbacks(app)
register_line_chart_callbacks(app)
register_choropleth_callbacks(app)
register_predictive_modeling_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
