import pandas as pd
import plotly.express as px
from dash import dcc, html, Input, Output

# Load the dataset
df = pd.read_csv("data/global_temperature.csv")

# Layout for the line chart feature
def get_line_chart_layout():
    return html.Div([
        html.H2("Line Chart: Global Temperature Trends"),

        # Year range slider
        html.Label("Select Year Range:"),
        dcc.RangeSlider(
            id="line-year-slider",
            min=df["Year"].min(),
            max=df["Year"].max(),
            step=1,
            marks={year: str(year) for year in range(df["Year"].min(), df["Year"].max() + 1, 5)},
            value=[df["Year"].min(), df["Year"].max()],
        ),

        # Dropdown for line style selection
        html.Label("Select Line Style:"),
        dcc.Dropdown(
            id="line-style-selector",
            options=[
                {"label": "Solid", "value": "solid"},
                {"label": "Dash", "value": "dash"},
                {"label": "Dot", "value": "dot"}
            ],
            value="solid",
            clearable=False,
        ),

        # Graph display
        dcc.Graph(id="line-chart-graph"),
    ])

# Callback for the line chart
def register_line_chart_callbacks(app):
    @app.callback(
        Output("line-chart-graph", "figure"),
        [Input("line-year-slider", "value"),
         Input("line-style-selector", "value")]
    )
    def update_line_chart(year_range, selected_line_style):
        # Filter data based on selected year range
        filtered_data = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]

        # Aggregate data by year
        annual_data = filtered_data.groupby("Year")["Monthly Anomaly"].mean().reset_index()

        # Create the line chart
        fig = px.line(
            annual_data,
            x="Year",
            y="Monthly Anomaly",
            labels={"Monthly Anomaly": "Temperature Anomaly (°C)", "Year": "Year"},
            title="Global Annual Temperature Anomaly",
        )
        # Customize line style
        fig.update_traces(line=dict(dash=selected_line_style))
        return fig
