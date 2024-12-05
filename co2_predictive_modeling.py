import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

# Load the dataset
df = pd.read_csv("data/co2_emissions.csv")

# Group and structure data
df = df.groupby(["country_code", "country_name", "year"])["value"].mean().reset_index()

# Default settings
DEFAULT_COUNTRY_CODE = "USA"
DEFAULT_YEAR = 2033

# Layout for predictive modeling
def get_co2_predictive_modeling_layout():
    return html.Div([
        html.H2("Predictive Modeling: CO2 Emissions"),

        # Graph display
        dcc.Graph(id="co2-predictive-model-graph"),

        # Dropdown and input controls
        html.Div([
            html.Div([
                html.Label("Select a Country:"),
                dcc.Dropdown(
                    id="country-dropdown",
                    options=[
                        {"label": country, "value": code}
                        for code, country in df.groupby(["country_code", "country_name"]).size().index
                    ],
                    value=DEFAULT_COUNTRY_CODE,
                    placeholder="Select a country",
                    style={"marginBottom": "10px", "width": "100%"},
                ),
            ], style={"flex": "1", "paddingRight": "10px"}),

            html.Div([
                html.Label("Enter a Future Year for Prediction:"),
                dcc.Input(
                    id="forecast-year-input",
                    type="number",
                    value=DEFAULT_YEAR,
                    min=df["year"].max(),
                    style={"marginBottom": "10px", "width": "100%"},
                ),
            ], style={"flex": "1", "paddingLeft": "10px"}),
        ], style={"display": "flex", "marginBottom": "20px"}),

    ], style={"padding": "20px"})

# Callback for predictive modeling
def register_co2_predictive_modeling_callbacks(app):
    @app.callback(
        Output("co2-predictive-model-graph", "figure"),
        [Input("country-dropdown", "value"), Input("forecast-year-input", "value")]
    )
    def update_co2_predictive_model(country_code, target_year):
        # Use default values if no input
        if not country_code:
            country_code = DEFAULT_COUNTRY_CODE
        if not target_year:
            target_year = DEFAULT_YEAR

        country_data = df[df["country_code"] == country_code]
        if country_data.empty:
            return go.Figure().update_layout(title="No data available for the selected country.")

        # Validate target year
        if target_year <= country_data["year"].max():
            target_year = country_data["year"].max() + 1

        # SARIMA Model
        model = SARIMAX(country_data["value"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        model_fit = model.fit(disp=False)

        forecast_start = country_data["year"].max()
        forecast_steps = target_year - forecast_start + 1
        forecast = model_fit.get_forecast(steps=forecast_steps)
        forecast_ci = forecast.conf_int(alpha=0.10)

        forecast_years = list(range(forecast_start, target_year + 1))

        # Initialize figure
        fig = go.Figure()

        # Historical data
        fig.add_trace(go.Scatter(
            x=country_data["year"],
            y=country_data["value"],
            mode="lines",
            name="Historical Data",
        ))

        # Forecasted data
        fig.add_trace(go.Scatter(
            x=forecast_years,
            y=forecast.predicted_mean,
            mode="lines",
            name="Forecast",
        ))

        # Confidence interval
        fig.add_trace(go.Scatter(
            x=forecast_years + forecast_years[::-1],
            y=list(forecast_ci.iloc[:, 0]) + list(forecast_ci.iloc[:, 1])[::-1],
            fill="toself",
            name="Confidence Interval",
            mode="lines",
            line_color="rgba(0,0,0,0)",
        ))

        # Update layout
        fig.update_layout(
            title=f"CO2 Emissions Forecast for {country_data['country_name'].iloc[0]} (Up to {target_year})",
            xaxis_title="Year",
            yaxis_title="CO2 Emissions",
            template="plotly_white",
        )

        return fig
