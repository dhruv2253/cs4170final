import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("data/global_temperature.csv")

# Pivot the data for the heatmap
heatmap_data = df.pivot(index="Year", columns="Month", values="Monthly Anomaly")

# Create the heatmap using Plotly
fig = px.imshow(
    heatmap_data,
    labels=dict(x="Month", y="Year", color="Temperature Anomaly (°C)"),
    x=[str(i) for i in range(1, 13)],  # Convert months to strings
    color_continuous_scale="thermal",
    title="Monthly Temperature Anomalies by Year",
)

# Adjust the layout to make the cells square
fig.update_layout(
    autosize=False,
    width=800,  # Adjust width to control overall figure size
    height=800,  # Adjust height to control cell aspect ratio
    xaxis=dict(
        tickmode="array",
        tickvals=list(range(12)),
        ticktext=[str(i + 1) for i in range(12)],
    ),
    yaxis=dict(
        scaleanchor="x",  # Makes cells square
    ),
)

# Initialize the Dash app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
    html.H1("Global Climate Dashboard"),
    dcc.Graph(figure=fig)
], fluid=True)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
