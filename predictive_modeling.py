import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from dash import dcc, html

# Load the dataset
df = pd.read_csv("data/global_temperature.csv")
df = df.groupby("Year")["Monthly Anomaly"].mean().reset_index()  # Aggregate to yearly data

# Train-Test Split
train = df[df["Year"] <= 2000]
test = df[df["Year"] > 2000]

# Train a SARIMA Model
model = SARIMAX(train["Monthly Anomaly"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
model_fit = model.fit(disp=False)

# Forecast Future Values
forecast_steps = len(test)
forecast = model_fit.get_forecast(steps=forecast_steps)
forecast_ci = forecast.conf_int()

# Layout for the predictive modeling feature
def get_predictive_modeling_layout():
    return html.Div([
        html.H2("Predictive Modeling: Temperature Anomalies"),

        # Input field for user-specified year
        html.Label("Enter a Future Year for Prediction:"),
        dcc.Input(
            id="forecast-year-input",
            type="number",
            placeholder="Enter year (e.g., 2050)",
            min=df["Year"].max(),
            value=df["Year"].max() + 10,
            style={"marginBottom": "20px", "width": "100%"}
        ),

        # Graph display
        dcc.Graph(id="predictive-model-graph"),
    ])

# Callback for predictive modeling
def register_predictive_modeling_callbacks(app):
    @app.callback(
        Output("predictive-model-graph", "figure"),
        [Input("forecast-year-input", "value")]
    )
    def update_predictive_model(target_year):
        # Validate the target year
        if target_year is None or target_year <= df["Year"].max():
            target_year = df["Year"].max() + 1

        # Calculate forecast steps
        forecast_start = df["Year"].max()
        forecast_steps = max(0, target_year - forecast_start + 1)

        # Initialize the figure
        fig = go.Figure()

        # Plot historical data
        fig.add_trace(go.Scatter(
            x=df["Year"],
            y=df["Monthly Anomaly"],
            mode="lines",
            name="Historical Data",
        ))

        if forecast_steps > 0:
            # Train the SARIMA model with full historical data
            model = SARIMAX(df["Monthly Anomaly"], order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
            model_fit = model.fit(disp=False)

            # Forecast future values
            forecast = model_fit.get_forecast(steps=forecast_steps)
            forecast_years = list(range(forecast_start, target_year + 1))
            forecast_ci = forecast.conf_int()

            # Add forecast to the plot
            fig.add_trace(go.Scatter(
                x=forecast_years,
                y=forecast.predicted_mean,
                mode="lines",
                name="Forecast",
            ))

            # Add confidence interval
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
            title=f"Temperature Anomaly Forecast up to {target_year}",
            xaxis_title="Year",
            yaxis_title="Temperature Anomaly (°C)",
            template="plotly_white",
        )

        return fig
