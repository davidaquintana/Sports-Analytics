
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from scipy.stats import norm

# Load data
data = pd.read_csv('noah_schultz_advanced_csv.csv')

# Filter for 2023 and 2024
historical_data = data[data['Year'].isin([2023, 2024])]

# Bayesian Updating for ERA Projection
def bayesian_update(prior_mean, prior_std, observed_mean, observed_std, n_obs):
    posterior_var = 1 / (1 / prior_std**2 + n_obs / observed_std**2)
    posterior_mean = posterior_var * (prior_mean / prior_std**2 + n_obs * observed_mean / observed_std**2)
    posterior_std = np.sqrt(posterior_var)
    return posterior_mean, posterior_std

# Prior ERA (2023 Stats)
prior_mean = historical_data['ERA'].mean()
prior_std = historical_data['ERA'].std()

# Observed (2024 Stats)
observed_mean = historical_data.loc[historical_data['Year'] == 2024, 'ERA'].mean()
observed_std = historical_data.loc[historical_data['Year'] == 2024, 'ERA'].std()
n_obs = len(historical_data[historical_data['Year'] == 2024])

# Bayesian Update for ERA
posterior_mean, posterior_std = bayesian_update(prior_mean, prior_std, observed_mean, observed_std, n_obs)
print(f"Projected ERA: {posterior_mean:.2f} ± {posterior_std:.2f}")

# LSTM for Time Series Prediction
# Prepare data
def prepare_data(series, n_lags):
    X, y = [], []
    for i in range(len(series) - n_lags):
        X.append(series[i:i+n_lags])
        y.append(series[i+n_lags])
    return np.array(X), np.array(y)

# Features to predict
features = ['Innings_Pitched', 'Strikeouts', 'Walks', 'ERA', 'Pitch_Velocity_Avg']
predictions = {}

for feature in features:
    series = historical_data[feature].values
    n_lags = 5  # Number of previous games to use
    X, y = prepare_data(series, n_lags)

    # Reshape for LSTM
    X = X.reshape((X.shape[0], X.shape[1], 1))

    # Define LSTM model
    model = Sequential([
        LSTM(50, activation='relu', input_shape=(n_lags, 1)),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')

    # Fit model
    model.fit(X, y, epochs=50, verbose=0)

    # Predict future values (2025 projections)
    last_sequence = series[-n_lags:].reshape((1, n_lags, 1))
    prediction = model.predict(last_sequence)
    predictions[feature] = prediction[0, 0]

# Display results
print("2025 Projections:")
for feature, value in predictions.items():
    print(f"{feature}: {value:.2f}")

# Visualize
plt.figure(figsize=(10, 6))
for feature, value in predictions.items():
    plt.bar(feature, value, label=feature)
plt.title("Noah Schultz 2025 Projections")
plt.ylabel("Stat Value")
plt.legend()
plt.show()
