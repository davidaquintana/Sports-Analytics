# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV data into a DataFrame (replace 'file_path.csv' with your file path)
data = pd.read_csv("C:/Users/david/OneDrive/Desktop/Misc/Code/Sports  Analytics/GC vs Ripon/GC v Ripon CSV(Sheet1).csv")

# Standardize 'Yard Line' if not already done (assuming this is already done in your previous code)
def standardize_yard_line(row):
    if row['Yard Line'] > 50:
        return 50 + (50 - (row['Yard Line'] - 50))  # Convert opponent half to standardized format (51-100)
    return row['Yard Line']

data['Standardized_Yard_Line'] = data.apply(standardize_yard_line, axis=1)

# Simplified Expected Points (EP) Model
# Creating a basic EP model based on standardized yard line
# Note: In a real application, use a detailed EP model based on historical data

def get_expected_points(yard_line, down):
    """
    Returns expected points based on field position and down.
    This is a simplified model; replace with actual EP lookup table or model for accurate results.
    """
    if yard_line <= 20:
        return 0.5  # Own territory, low scoring chance
    elif 20 < yard_line <= 50:
        return 1.5  # Midfield, moderate scoring chance
    elif 50 < yard_line <= 80:
        return 3.0  # Opponent territory, higher scoring chance
    elif 80 < yard_line <= 100:
        return 6.0  # Red zone, very high scoring chance
    return 0  # Default

# Calculate EP before and after each play
data['EP_Before'] = data.apply(lambda row: get_expected_points(row['Standardized_Yard_Line'], row['Down']), axis=1)

# Calculate new field position after the play
data['New_Yard_Line'] = data['Standardized_Yard_Line'] + data['Yards Gained']

# Ensure new yard line is within field bounds (0-100)
data['New_Yard_Line'] = data['New_Yard_Line'].clip(lower=0, upper=100)

# Calculate EP after the play
data['EP_After'] = data.apply(lambda row: get_expected_points(row['New_Yard_Line'], row['Down']), axis=1)

# Calculate EPA
data['EPA'] = data['EP_After'] - data['EP_Before']

# Scatter Plot: EPA vs. Standardized Yard Line
plt.figure(figsize=(12, 6))
sns.scatterplot(x='Standardized_Yard_Line', y='EPA', hue='Personel', data=data, palette='viridis', s=100)
plt.title('EPA by Standardized Yard Line')
plt.xlabel('Standardized Yard Line')
plt.ylabel('EPA')
plt.axhline(0, color='red', linestyle='--', lw=1)  # Highlight zero EPA line
plt.legend(title='Formation', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
