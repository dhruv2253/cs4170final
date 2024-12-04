import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output

# Load the dataset
df = pd.read_csv("data/global_temperature.csv")

# Pivot the data for the heatmap
heatmap_data = df.pivot(index="Year", columns="Month", values="Monthly Anomaly")

# List of available color scales for the heatmap
color_scales = [
    "thermal", "viridis", "cividis", "magma", "plasma",
    "inferno", "blues", "greens", "reds", "purples"
]


# Layout for the heatmap feature
def get_heatmap_layout():
    return html.Div([
        html.H2("Heatmap: Temperature Anomalies"),

        # Dropdown for color theme selection
        html.Label("Select Color Theme:"),
        dcc.Dropdown(
            id="color-theme-selector",
            options=[{"label": scale.capitalize(), "value": scale} for scale in color_scales],
            value="thermal",
            clearable=False,
        ),

        # RangeSlider for date selection
        html.Label("Select Year Range:"),
        dcc.RangeSlider(
            id="year-slider",
            min=heatmap_data.index.min(),
            max=heatmap_data.index.max(),
            step=1,
            marks={year: str(year) for year in range(heatmap_data.index.min(), heatmap_data.index.max() + 1, 5)},
            value=[heatmap_data.index.min(), heatmap_data.index.max()],
        ),

        # Graph display
        dcc.Graph(id="climate-graph"),
    ])


# Callback for the heatmap
def register_heatmap_callbacks(app):
    @app.callback(
        Output("climate-graph", "figure"),
        [Input("year-slider", "value"),
         Input("color-theme-selector", "value")]
    )
    def update_graph(year_range, selected_color_theme):
        # Filter heatmap data based on selected year range
        filtered_data = heatmap_data.loc[year_range[0]:year_range[1]]

        # Create heatmap with selected color theme
        fig = px.imshow(
            filtered_data,
            labels=dict(x="Month", y="Year", color="Temperature Anomaly (°C)"),
            x=[str(i) for i in range(1, 13)],  # Convert months to strings
            color_continuous_scale=selected_color_theme,
            title="Monthly Temperature Anomalies by Year",
        )
        # Adjust layout for square cells
        fig.update_layout(
            autosize=False,
            width=800,
            height=800,
            xaxis=dict(tickmode="array", tickvals=list(range(12)), ticktext=[str(i + 1) for i in range(12)]),
            yaxis=dict(scaleanchor="x"),
        )
        return fig
