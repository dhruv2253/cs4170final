import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output

# Load the CO2 emissions dataset
df = pd.read_csv("data/co2_emissions.csv")

# Layout for the choropleth map feature
def get_choropleth_layout():
    return html.Div([
        html.H2("Choropleth Map: Global CO₂ Emissions"),

        # Year range slider
        html.Label("Select Year Range:"),
        dcc.RangeSlider(
            id="choropleth-year-slider",
            min=df["year"].min(),
            max=df["year"].max(),
            step=1,
            marks={year: str(year) for year in range(df["year"].min(), df["year"].max() + 1, 5)},
            value=[df["year"].min(), df["year"].max()],
        ),

        # Graph display
        dcc.Graph(id="choropleth-map"),
    ])

# Callback for the choropleth map
def register_choropleth_callbacks(app):
    @app.callback(
        Output("choropleth-map", "figure"),
        [Input("choropleth-year-slider", "value")]
    )
    def update_choropleth(year_range):
        # Filter data by the selected year range
        filtered_data = df[(df["year"] >= year_range[0]) & (df["year"] <= year_range[1])]

        # Aggregate data by country within the selected year range
        aggregated_data = (
            filtered_data.groupby(["country_code", "country_name"])["value"]
            .mean()
            .reset_index()
        )

        # Create the choropleth map
        fig = px.choropleth(
            aggregated_data,
            locations="country_code",  # ISO 3166-1 alpha-3 country codes
            color="value",
            hover_name="country_name",
            title=f"Average CO₂ Emissions ({year_range[0]}–{year_range[1]})",
            color_continuous_scale="Viridis",
            labels={"value": "Average CO₂ Emissions (kt)"},
        )
        fig.update_layout(
            geo=dict(showframe=False, showcoastlines=True, projection_type="equirectangular"),
            margin={"r": 0, "t": 40, "l": 0, "b": 0},
        )
        return fig

