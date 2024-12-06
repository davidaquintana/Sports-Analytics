
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = '1985_chicago_bears.csv'
data = pd.read_csv(file_path)

# Separate regular season and postseason
regular_season = data[data['Game'].str.startswith('Post') == False]
postseason = data[data['Game'].str.startswith('Post')]

# Plot 1: Points Scored vs. Points Allowed
plt.figure(figsize=(10, 6))
plt.plot(regular_season['Game'], regular_season['Points_Scored'], label='Points Scored', marker='o')
plt.plot(regular_season['Game'], regular_season['Points_Allowed'], label='Points Allowed', marker='x')
plt.title('1985 Chicago Bears: Points Scored vs. Points Allowed')
plt.xlabel('Game')
plt.ylabel('Points')
plt.legend()
plt.grid()

# Plot 2: Turnover Differential
plt.figure(figsize=(10, 6))
plt.bar(regular_season['Game'], regular_season['Turnover_Differential'], color='orange')
plt.title('1985 Chicago Bears: Turnover Differential')
plt.xlabel('Game')
plt.ylabel('Turnover Differential')
plt.axhline(0, color='black', linewidth=0.8)
plt.grid(axis='y')

# Plot 3: Rushing vs. Passing Yards
plt.figure(figsize=(10, 6))
plt.plot(regular_season['Game'], regular_season['Passing_Yards'], label='Passing Yards', marker='o')
plt.plot(regular_season['Game'], regular_season['Rushing_Yards'], label='Rushing Yards', marker='x')
plt.title('1985 Chicago Bears: Passing vs. Rushing Yards')
plt.xlabel('Game')
plt.ylabel('Yards')
plt.legend()
plt.grid()

# Plot 4: Postseason Performance
plt.figure(figsize=(10, 6))
plt.bar(postseason['Game'], postseason['Points_Scored'], label='Points Scored', color='blue', alpha=0.7)
plt.bar(postseason['Game'], postseason['Points_Allowed'], label='Points Allowed', color='red', alpha=0.7)
plt.title('1985 Chicago Bears: Postseason Performance')
plt.xlabel('Game')
plt.ylabel('Points')
plt.legend()
plt.grid(axis='y')

plt.savefig("passing_vs_rushing.svg", format="svg")


# Show all plots
plt.tight_layout()
plt.show()
