import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("data/global_temperature.csv")

# Pivot the data for the heatmap
heatmap_data = df.pivot(index="Year", columns="Month", values="Monthly Anomaly")

# Initialize the Dash app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define layout with interactivity components
app.layout = dbc.Container([
    html.H1("Global Climate Dashboard"),

    # Dropdown for graph selection
    html.Label("Select Graph:"),
    dcc.Dropdown(
        id="graph-selector",
        options=[{"label": "Temperature Anomalies Heatmap", "value": "heatmap"}],
        value="heatmap",
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
], fluid=True)


# Callback to update the graph based on user input
@app.callback(
    Output("climate-graph", "figure"),
    [Input("graph-selector", "value"),
     Input("year-slider", "value")]
)
def update_graph(selected_graph, year_range):
    # Filter heatmap data based on selected year range
    filtered_data = heatmap_data.loc[year_range[0]:year_range[1]]

    if selected_graph == "heatmap":
        # Create heatmap
        fig = px.imshow(
            filtered_data,
            labels=dict(x="Month", y="Year", color="Temperature Anomaly (°C)"),
            x=[str(i) for i in range(1, 13)],  # Convert months to strings
            color_continuous_scale="thermal",
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

    # Default empty figure (can add more graphs in the future)
    return {}


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
