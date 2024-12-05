import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
from global_temp_model import evaluate_model  # Import the evaluate_model function

from heatmap import get_heatmap_layout, register_heatmap_callbacks
from line_chart import get_line_chart_layout, register_line_chart_callbacks
from choropleth import get_choropleth_layout, register_choropleth_callbacks
from predictive_modeling import get_predictive_modeling_layout, register_predictive_modeling_callbacks
from co2_predictive_modeling import (
    get_co2_predictive_modeling_layout,
    register_co2_predictive_modeling_callbacks,
)

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Suppress callback exceptions for dynamic layouts
app.config.suppress_callback_exceptions = True

# Define the layout for model evaluation
def get_model_evaluation_layout(mse, r2, coefficients):
    # Create a more comprehensive and visually appealing model evaluation layout
    explanation = html.Div([
        html.H3("Global Temperature Linear Regression Model Evaluation", className="mb-4"),

        # Model Performance Overview Card
        dbc.Card([
            dbc.CardHeader(html.H4("Model Performance Metrics", className="text-center")),
            dbc.CardBody([
                # MSE Explanation
                html.Div([
                    html.H5("Mean Squared Error (MSE)", className="text-primary"),
                    html.P(f"{mse:.4f}", className="lead text-success"),
                    html.Small(
                        "MSE measures the average squared difference between predicted and actual values. "
                        "Lower values indicate more accurate predictions.",
                        className="text-muted"
                    )
                ], className="mb-3"),
            ])
        ], className="mb-4"),

        # Feature Coefficients Card
        dbc.Card([
            dbc.CardHeader(html.H4("Feature Coefficients Analysis", className="text-center")),
            dbc.CardBody([
                html.P(
                    "Coefficients show how each feature impacts the Annual Temperature Anomaly. "
                    "Positive values increase the anomaly, negative values decrease it.",
                    className="mb-3"
                ),
                dbc.Table(
                    [
                        html.Thead(
                            html.Tr([
                                html.Th("Feature"),
                                html.Th("Coefficient"),
                                html.Th("Interpretation")
                            ])
                        ),
                        html.Tbody([
                            html.Tr([
                                html.Td(feature),
                                html.Td(f"{coef:.4f}", className="text-primary"),
                                html.Td(
                                    "Positive increase" if coef > 0 else "Negative influence",
                                    className="text-success" if coef > 0 else "text-warning"
                                )
                            ]) for feature, coef in coefficients.items()
                        ])
                    ],
                    striped=True,
                    hover=True,
                    responsive=True
                )
            ])
        ])
    ])

    return explanation

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
                        {"label": "Global Temperature Predictive Modeling", "value": "predictive_modeling"},
                        {"label": "Model Evaluation on Global Temperatures", "value": "analysis"},
                        {"label": "Co2 Emissions Predictive Modeling", "value": "co2_predictive_modeling"},
                    ],
                    value="heatmap",  # Default value
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
        return get_predictive_modeling_layout()
    elif feature == "analysis":
        # Run model evaluation when "Analysis" is selected
        mse, r2, coefficients = evaluate_model()  # Call evaluate_model from global_temp_model.py
        return get_model_evaluation_layout(mse, r2, coefficients)  # Display model evaluation results
    elif feature == "co2_predictive_modeling":
        return get_co2_predictive_modeling_layout()
    return html.Div("Select a valid feature.")

# Register callbacks for each feature
register_heatmap_callbacks(app)
register_line_chart_callbacks(app)
register_choropleth_callbacks(app)
register_predictive_modeling_callbacks(app)
register_co2_predictive_modeling_callbacks(app)  # Register CO2 Predictive Modeling Callbacks

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
