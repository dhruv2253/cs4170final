import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.impute import SimpleImputer


def evaluate_model():
    """
    Performs model evaluation on global temperature data using time series cross-validation.

    Returns:
    - Mean Squared Error (MSE)
    - R-squared Score
    - Feature Coefficients Dictionary
    """
    # Load the dataset
    df = pd.read_csv('data/global_temperature.csv')

    # Handle missing values using imputation
    imputer = SimpleImputer(strategy='mean')
    df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

    # Create a proper date column with type conversion
    df_imputed['Year'] = df_imputed['Year'].astype(int)
    df_imputed['Month'] = df_imputed['Month'].astype(int)

    # Create a date column using pandas to_datetime with explicit formatting
    df_imputed['Date'] = pd.to_datetime(
        df_imputed['Year'].astype(str) + '-' +
        df_imputed['Month'].astype(str).str.zfill(2) +
        '-01'  # Add a day to make it a valid date
    )

    # Sort the dataframe by date to ensure chronological order
    df_imputed = df_imputed.sort_values('Date')

    # Create feature set and target variable
    features = ['Monthly Anomaly', 'Five-Year Anomaly', 'Ten-Year Anomaly', 'Twenty-Year Anomaly']
    X = df_imputed[features]
    y = df_imputed['Annual Anomaly']

    # Initialize TimeSeriesSplit
    tscv = TimeSeriesSplit(n_splits=5)

    # Prepare lists to store performance metrics
    mse_scores = []
    r2_scores = []
    mae_scores = []

    # Standardization scaler
    scaler = StandardScaler()

    # Perform cross-validation
    for train_index, test_index in tscv.split(X):
        # Split data while maintaining time order
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        # Scale the features
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train the model
        model = LinearRegression()
        model.fit(X_train_scaled, y_train)

        # Predict and evaluate
        y_pred = model.predict(X_test_scaled)

        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)

        # Store metrics
        mse_scores.append(mse)
        r2_scores.append(r2)
        mae_scores.append(mae)

    # Calculate average performance metrics
    mean_mse = np.mean(mse_scores)
    mean_r2 = np.mean(r2_scores)

    # Final model for coefficient analysis
    X_scaled = scaler.fit_transform(X)
    final_model = LinearRegression()
    final_model.fit(X_scaled, y)

    # Create coefficients dictionary
    coefficients = dict(zip(features, final_model.coef_))

    # Print results for logging
    print("Time Series Cross-Validation Results:")
    print(f"Mean Squared Error: {mean_mse:.4f}")
    print(f"R-squared Score: {mean_r2:.4f}")

    print("\nFeature Importance:")
    for feature, coef in coefficients.items():
        print(f"{feature}: {coef:.4f}")

    # Return key metrics for UI display
    return mean_mse, mean_r2, coefficients

# Uncomment the line below if you want to run the evaluation when the script is executed directly
evaluate_model()