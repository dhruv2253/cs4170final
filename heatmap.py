import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("data/global_temperature.csv")

# Pivot the data to create a heatmap matrix
heatmap_data = df.pivot(index="Year", columns="Month", values="Monthly Anomaly")

# Set the plot size
plt.figure(figsize=(12, 8))

# Create the heatmap
sns.heatmap(
    heatmap_data,
    cmap="coolwarm",  # Color scheme
    annot=False,      # Set to True for numerical values
    cbar_kws={'label': 'Temperature Anomaly (°C)'}
)

# Add labels and title
plt.title("Monthly Temperature Anomalies by Year")
plt.xlabel("Month")
plt.ylabel("Year")

# Display the plot
plt.show()
