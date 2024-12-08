
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
file_path = 'noah_schultz_pitching.csv'
data = pd.read_csv(file_path)

# Plot 1: Innings Pitched per Game
plt.figure(figsize=(10, 6))
plt.plot(data['Game'], data['Innings_Pitched'], marker='o', label='Innings Pitched')
plt.title('Noah Schultz: Innings Pitched per Game')
plt.xlabel('Game')
plt.ylabel('Innings Pitched')
plt.grid()
plt.legend()

# Plot 2: Strikeouts and Walks per Game
plt.figure(figsize=(10, 6))
plt.plot(data['Game'], data['Strikeouts'], marker='o', label='Strikeouts')
plt.plot(data['Game'], data['Walks'], marker='x', label='Walks', color='orange')
plt.title('Noah Schultz: Strikeouts and Walks per Game')
plt.xlabel('Game')
plt.ylabel('Count')
plt.grid()
plt.legend()

# Plot 3: Earned Runs per Game
plt.figure(figsize=(10, 6))
plt.bar(data['Game'], data['Earned_Runs'], color='red', alpha=0.7)
plt.title('Noah Schultz: Earned Runs per Game')
plt.xlabel('Game')
plt.ylabel('Earned Runs')
plt.grid(axis='y')

# Plot 4: Pitch Velocity (Average)
plt.figure(figsize=(10, 6))
plt.plot(data['Game'], data['Pitch_Velocity_Avg'], marker='o', label='Average Pitch Velocity', color='green')
plt.title('Noah Schultz: Average Pitch Velocity')
plt.xlabel('Game')
plt.ylabel('Velocity (mph)')
plt.grid()
plt.legend()

# Show all plots
plt.tight_layout()
plt.show()
