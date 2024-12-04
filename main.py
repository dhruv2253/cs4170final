import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
from heatmap import get_heatmap_layout, register_heatmap_callbacks

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Suppress callback exceptions for dynamic layouts
app.config.suppress_callback_exceptions = True

# Define the main layout
app.layout = dbc.Container([
    html.H1("Global Climate Dashboard"),

    # Navigation or Section Heading
    html.Div([
        html.H2("Select a Feature:"),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id="feature-selector",
                    options=[
                        {"label": "Heatmap", "value": "heatmap"},
                        # Add more options for other features as needed
                    ],
                    value="heatmap",
                    clearable=False,
                    style={"width": "100%"}
                ),
                width=12,
            )
        ])
    ], style={"marginBottom": "20px"}),

    # Dynamic Content Placeholder
    html.Div(id="feature-content"),
], fluid=True)  # Use fluid layout to avoid horizontal scrolling


# Callback to dynamically load content based on selected feature
@app.callback(
    Output("feature-content", "children"),
    [Input("feature-selector", "value")]
)
def display_feature(feature):
    if feature == "heatmap":
        return get_heatmap_layout()  # load heatmap layout
    # Add more conditions for other features
    return html.Div("Select a valid feature.")


# Register callbacks for each feature
register_heatmap_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
