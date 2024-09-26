# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the CSV data into a DataFrame (replace 'file_path.csv' with your file path)
data = pd.read_csv(r'C:\Users\david\OneDrive\Desktop\Misc\Code\Sports  Analytics\GC v Ripon CSV(Sheet1).csv')

# Data Cleaning and Preprocessing
# Remove any extraneous or unnecessary columns
# Drop rows with missing critical values if necessary

# Convert 'Yard Line' to standardized representation
# Assuming the 'Yard Line' column represents yards from own end zone (0-50) and needs conversion for opponent's half
def standardize_yard_line(row):
    if row['Yard Line'] > 50:
        return 50 + (50 - (row['Yard Line'] - 50))  # Convert opponent half to standardized format (51-100)
    return row['Yard Line']

data['Standardized_Yard_Line'] = data.apply(standardize_yard_line, axis=1)

# Fill missing 'Play Call' values with a placeholder (e.g., 'Unknown')
data['Play Call'].fillna('Unknown', inplace=True)

# Define a function to determine play success based on down and distance
def calculate_play_success(down, distance, yards_gained):
    """
    Determines if a play is successful based on down, distance, and yards gained.
    Returns 1 for success, 0 for failure.
    """
    if down == 1:
        # Success if gain is 50% or more of needed yardage on 1st down
        return 1 if yards_gained >= 0.5 * distance else 0
    elif down == 2:
        # Success if gain is 70% or more of needed yardage on 2nd down
        return 1 if yards_gained >= 0.7 * distance else 0
    elif down in [3, 4]:
        # Success if gain is 100% of needed yardage on 3rd/4th down
        return 1 if yards_gained >= distance else 0
    else:
        return 0  # Unlikely case, but a safeguard for invalid data

# Apply the function to create a new column 'Play_Success'
data['Play_Success'] = data.apply(
    lambda row: calculate_play_success(row['Down'], row['Yards to Go'], row['Yards Gained']), 
    axis=1
)

# Group data by formation and calculate success rates and average yards gained
formation_analysis = data.groupby('Personel').agg({
    'Play_Success': 'mean',
    'Yards Gained': 'mean',
    'Play Call': 'count'
}).reset_index()
formation_analysis.columns = ['Formation', 'Success Rate', 'Avg Yards Gained', 'Play Count']

# Display the formation analysis sorted by success rate
print(formation_analysis.sort_values(by='Success Rate', ascending=False))

# Visualization: Success Rate by Formation
plt.figure(figsize=(12, 6))
sns.barplot(x='Formation', y='Success Rate', data=formation_analysis)
plt.title('Play Success Rate by Formation')
plt.xlabel('Formation')
plt.ylabel('Success Rate')
plt.xticks(rotation=45)
plt.show()

# Visualization: Average Yards Gained by Formation
plt.figure(figsize=(12, 6))
sns.barplot(x='Formation', y='Avg Yards Gained', data=formation_analysis)
plt.title('Average Yards Gained by Formation')
plt.xlabel('Formation')
plt.ylabel('Average Yards Gained')
plt.xticks(rotation=45)
plt.show()

# Additional Analysis: Success Rate by Down
down_analysis = data.groupby('Down').agg({
    'Play_Success': 'mean',
    'Yards Gained': 'mean'
}).reset_index()
print(down_analysis)

# Visualization: Success Rate by Down
plt.figure(figsize=(8, 6))
sns.barplot(x='Down', y='Play_Success', data=down_analysis)
plt.title('Play Success Rate by Down')
plt.xlabel('Down')
plt.ylabel('Success Rate')
plt.show()

# Visualization: Average Yards Gained by Down
plt.figure(figsize=(8, 6))
sns.barplot(x='Down', y='Yards Gained', data=down_analysis)
plt.title('Average Yards Gained by Down')
plt.xlabel('Down')
plt.ylabel('Average Yards Gained')
plt.show()

# Check for 'Drive Number' column, if not present, create it based on your logic
if 'Drive Number' not in data.columns:
    data['Drive Number'] = 0  # Initialize with zeros
    drive_number = 1
    for index, row in data.iterrows():
        if row['Play Call'] in ['Kickoff', 'Punt'] or index == 0:
            drive_number += 1
        data.at[index, 'Drive Number'] = drive_number

# Drive Efficiency Analysis
drive_analysis = data.groupby('Drive Number').agg({
    'Play Call': 'count',                # Number of plays in the drive
    'Yards Gained': 'sum',               # Total yards gained in the drive
    'Standardized_Yard_Line': 'first',   # Starting yard line of the drive
    'TD': 'sum',                         # Total touchdowns in the drive
    'Penalty': 'count'                   # Total penalties in the drive
}).reset_index()
drive_analysis.columns = ['Drive Number', 'Total Plays', 'Total Yards', 'Starting Yard Line', 'Total TDs', 'Total Penalties']

# Display the drive efficiency analysis
print(drive_analysis.sort_values(by='Total Yards', ascending=False))

# Visualization: Total Yards by Drive
plt.figure(figsize=(12, 6))
sns.barplot(x='Drive Number', y='Total Yards', data=drive_analysis)
plt.title('Total Yards by Drive')
plt.xlabel('Drive Number')
plt.ylabel('Total Yards')
plt.xticks(rotation=45)
plt.show()

# Third and Fourth Down Conversion Analysis
# Filter data for 3rd and 4th down plays
third_fourth_down_data = data[data['Down'].isin([3, 4])]

# Calculate conversion rates (successful conversions) and average yards needed
conversion_analysis = third_fourth_down_data.groupby('Down').agg({
    'Play_Success': 'mean',              # Conversion success rate
    'Yards to Go': 'mean',               # Average yards to go
    'Yards Gained': 'mean'               # Average yards gained
}).reset_index()
conversion_analysis.columns = ['Down', 'Conversion Rate', 'Avg Yards to Go', 'Avg Yards Gained']

# Display the third and fourth down conversion analysis
print(conversion_analysis)

# Visualization: Conversion Rate by Down
plt.figure(figsize=(8, 6))
sns.barplot(x='Down', y='Conversion Rate', data=conversion_analysis)
plt.title('Third and Fourth Down Conversion Rate')
plt.xlabel('Down')
plt.ylabel('Conversion Rate')
plt.show()

# Visualization: Average Yards to Go by Down
plt.figure(figsize=(8, 6))
sns.barplot(x='Down', y='Avg Yards to Go', data=conversion_analysis)
plt.title('Average Yards to Go on Third and Fourth Down')
plt.xlabel('Down')
plt.ylabel('Average Yards to Go')
plt.show()

# Visualization: Average Yards Gained by Down
plt.figure(figsize=(8, 6))
sns.barplot(x='Down', y='Avg Yards Gained', data=conversion_analysis)
plt.title('Average Yards Gained on Third and Fourth Down')
plt.xlabel('Down')
plt.ylabel('Average Yards Gained')
plt.show()
