import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Read the CSV file
df = pd.read_csv("C:/Users/david/OneDrive/Desktop/Misc/Code/Sports  Analytics/pitch_stats.csv")




# Show the first few rows to verify data
print(df.head())

# 1. Compare Expected vs Actual Metrics

# Plot comparison between Actual and Expected Batting Average (BA vs XBA)
df.plot(x='Pitch Type', y=['BA', 'XBA'], kind='bar', title='Actual vs Expected Batting Average', figsize=(10,6))
plt.show()

# Plot comparison between Actual and Expected Slugging Percentage (SLG vs XSLG)
df.plot(x='Pitch Type', y=['SLG', 'XSLG'], kind='bar', title='Actual vs Expected Slugging Percentage', figsize=(10,6))
plt.show()

# Plot comparison between Actual and Expected WOBA (WOBA vs XWOBA)
df.plot(x='Pitch Type', y=['WOBA', 'XWOBA'], kind='bar', title='Actual vs Expected WOBA', figsize=(10,6))
plt.show()

# 2. Whiff% vs Velocity (MPH)

# Scatter plot for Whiff% vs MPH
df.plot(kind='scatter', x='MPH', y='Whiff%', title='Whiff% vs Velocity (MPH)', color='red', figsize=(10,6))
plt.show()

# 3. Spin Rate Impact on SLG (Slugging Percentage)

# Scatter plot for Spin Rate vs SLG
df.plot(kind='scatter', x='Spin', y='SLG', title='Spin Rate vs Slugging Percentage', color='blue', figsize=(10,6))
plt.show()

# 4. Predicting Strikeouts Using Linear Regression

# Prepare data for regression (X = MPH, y = SO)
X = df[['MPH']]
y = df['SO']

# Create and train a Linear Regression model
model = LinearRegression()
model.fit(X, y)

# Predict the number of strikeouts
df['Predicted SO'] = model.predict(X)

# Compare actual vs predicted strikeouts
df.plot(x='Pitch Type', y=['SO', 'Predicted SO'], kind='bar', title='Actual vs Predicted Strikeouts', figsize=(10,6))
plt.show()

# Show the dataframe with predicted strikeouts for reference
import ace_tools as tools; tools.display_dataframe_to_user(name="Pitch Type Data with Predictions", dataframe=df)
