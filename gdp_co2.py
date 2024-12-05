from dash import html, dcc, Input, Output
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import plotly.graph_objects as go


# Load CO2 Emissions Data
def load_co2_data(co2_file):
    co2_df = pd.read_csv(co2_file)
    co2_df = co2_df[['country_name', 'year', 'value']]
    co2_df = co2_df.rename(columns={'value': 'co2_emissions'})
    return co2_df


# Load GDP Data
def load_gdp_data(gdp_file):
    gdp_df = pd.read_csv(gdp_file)
    if 'Unnamed: 65' in gdp_df.columns:
        gdp_df = gdp_df.drop(columns=['Unnamed: 65'])
    gdp_df = gdp_df.melt(id_vars=['country_name', 'country_code'],
                         var_name='year',
                         value_name='gdp')
    gdp_df['year'] = gdp_df['year'].astype(int)
    return gdp_df


# Merge CO2 and GDP Data
def merge_data(co2_df, gdp_df):
    merged_df = pd.merge(co2_df, gdp_df, on=['country_name', 'year'], how='inner')
    return merged_df


# Train the model
def train_model(merged_df):
    merged_df = merged_df.dropna(subset=['gdp', 'co2_emissions'])
    X = merged_df[['gdp']]
    y = merged_df['co2_emissions']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    return model, X_test, y_test, y_pred, merged_df


# Plot Results (Interactive Plotly Plot)
# Plot Results (Interactive Plotly Plot)
def plot_results(X_test, y_test, y_pred, merged_df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=X_test.values.flatten(),
        y=y_test,
        mode='markers',
        name='Actual Data',
        marker=dict(color='blue', size=12),
        text=merged_df.loc[X_test.index, 'country_name'],
        hoverinfo='text+x+y'
    ))

    fig.add_trace(go.Scatter(
        x=X_test.values.flatten(),
        y=y_pred,
        mode='lines',
        name='Linear Regression Line',
        line=dict(color='red', width=2),
    ))

    fig.update_layout(
        title="GDP vs CO2 Emissions 1960-2020",
        xaxis_title='GDP',
        yaxis_title='CO2 Emissions (in kilotons)',
        hovermode="closest",
        xaxis=dict(
            range=[X_test.values.min() * 0.9, X_test.values.max() * 1.1],
            linecolor='gray',  # Set x-axis line color to gray
            showgrid=True,  # Enable gridlines
            gridcolor='lightgray',  # Set gridline color to light gray
            gridwidth=1  # Set gridline width
        ),
        yaxis=dict(
            range=[y_test.min() * 0.9, y_test.max() * 1.1],
            linecolor='gray',  # Set y-axis line color to gray
            showgrid=True,  # Enable gridlines
            gridcolor='lightgray',  # Set gridline color to light gray
            gridwidth=1  # Set gridline width
        ),
        showlegend=True,

        # Set background color to white
        plot_bgcolor="white",  # Plot area background color
        paper_bgcolor="white",  # Whole paper background color
        font=dict(color="black")  # Font color to ensure text is readable
    )

    return fig

# Function for Dash Layout
def get_gdp_co2_predictive_modeling_layout(co2_file, gdp_file):
    co2_df = load_co2_data(co2_file)
    gdp_df = load_gdp_data(gdp_file)
    merged_df = merge_data(co2_df, gdp_df)
    model, X_test, y_test, y_pred, merged_df = train_model(merged_df)
    fig = plot_results(X_test, y_test, y_pred, merged_df)

    layout = html.Div([
        html.H3("CO2 Emissions and GDP Correlation"),
        html.P(
            "This section demonstrates the relationship between CO2 emissions and GDP using a linear regression model. "
            "Hover over the data points to see the corresponding country names."),
        dcc.Graph(
            id="gdp-co2-plot",
            figure=fig
        ),
        html.Div(
            id="country-info",  # Div to display the country information
            style={"marginTop": "20px", "fontSize": "18px"}
        )
    ])

    return layout


# Callback to update country info below the plot
def register_gdp_co2_predictive_modeling_callbacks(app):
    @app.callback(
        Output("country-info", "children"),
        [Input("gdp-co2-plot", "hoverData")]
    )
    def display_country_info(hoverData):
        if hoverData is None:
            return "Hover over a data point to see more details."

        # Extract trace information
        trace_type = hoverData['points'][0]['curveNumber']

        # Check if hoverData is from a scatter (data point) or line trace
        if 'text' in hoverData['points'][0]:  # Data points (scatter plot)
            country_name = hoverData['points'][0]['text']
            gdp_value = hoverData['points'][0]['x']
            co2_value = hoverData['points'][0]['y']

            # Format the information with separate lines for GDP and CO2 emissions
            return html.Div([
                html.P(f"Country: {country_name}"),
                html.P(f"GDP: ${gdp_value:,.2f}"),
                html.P(f"CO2 Emissions: {co2_value:,.2f} tons")
            ])

        elif trace_type == 1:  # If it's the regression line (assumed curveNumber 1)
            # For the regression line, we can show a generic message or any other relevant info
            return html.Div([
                html.P("Hover over the data points to see country-specific information.")
            ])
        else:
            return "Hover over a data point to see more details."



