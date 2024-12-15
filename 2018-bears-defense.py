# bears_defense_2018.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = {
    'Player': ['Khalil Mack', 'Akiem Hicks', 'Roquan Smith', 'Kyle Fuller', 'Eddie Jackson'],
    'Sacks': [12.5, 7.5, 5, 0, 0],
    'Interceptions': [0, 0, 1, 7, 6],
    'Forced Fumbles': [6, 3, 1, 0, 1],
    'Touchdowns': [1, 0, 1, 2, 3]
}

df = pd.DataFrame(data)

plt.figure(figsize=(10, 6))
sns.barplot(x='Player', y='Sacks', data=df, palette='Blues_d')
plt.title('2018 Chicago Bears Defensive Sacks')
plt.ylabel('Total Sacks')
plt.xlabel('Player')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))
sns.barplot(x='Player', y='Interceptions', data=df, palette='Greens_d')
plt.title('2018 Chicago Bears Defensive Interceptions')
plt.ylabel('Total Interceptions')
plt.xlabel('Player')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

df['Total Turnovers'] = df['Sacks'] + df['Interceptions']

plt.figure(figsize=(10, 6))
sns.barplot(x='Player', y='Total Turnovers', data=df, palette='Purples_d')
plt.title('2018 Chicago Bears Total Turnovers by Player')
plt.ylabel('Total Turnovers')
plt.xlabel('Player')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 8))
plt.pie(
    df['Touchdowns'], 
    labels=df['Player'], 
    autopct='%1.1f%%', 
    startangle=140, 
    colors=sns.color_palette('coolwarm', n_colors=5)
)
plt.title('2018 Chicago Bears Defensive Touchdowns')
plt.show()

# Step 5: Insights Across the Season (Optional)
# You can expand by plotting turnovers, points allowed, and other metrics over the 16-game season.
