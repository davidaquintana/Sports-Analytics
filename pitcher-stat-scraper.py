from pybaseball import statcast_pitcher, playerid_lookup
import pandas as pd

def fetch_season_stats(first_name, last_name, season):
    """
    Fetch game-by-game stats for the specified pitcher for the full MLB season.
    """
    print(f"Fetching stats for {first_name} {last_name} in the {season} season...")

    # Retrieve player ID
    player_info = playerid_lookup(last=last_name, first=first_name)
    if player_info.empty:
        raise ValueError(f"No player found with name {first_name} {last_name}.")
    player_id = player_info.iloc[0]['key_mlbam']

    # Define season start and end dates
    start_date = f"{season}-04-01"
    end_date = f"{season}-10-01"

    # Fetch pitch-level data
    pitch_data = statcast_pitcher(start_dt=start_date, end_dt=end_date, player_id=player_id)
    if pitch_data.empty:
        raise ValueError(f"No data found for {first_name} {last_name} in the {season} season.")

    # Inspect available columns
    print("Available columns in pitch data:")
    print(pitch_data.columns)

    # Debug: Inspect unique values in the 'events' column
    print("Unique values in 'events' column:")
    print(pitch_data['events'].unique())

    # Aggregate data to game level
    if 'opponent' in pitch_data.columns:
        game_stats = pitch_data.groupby(['game_date', 'opponent']).agg({
            'pitch_type': 'count',
            'release_speed': 'mean',
            'release_spin_rate': 'mean',
            'p_throws': 'first',
            'balls': 'sum',
            'strikes': 'sum',
            'events': lambda x: (x == 'strikeout').sum(),  # Count strikeouts using the 'events' column
            'description': lambda x: (x == 'home_run').sum()  # Count home runs using 'description'
        }).reset_index()
    else:
        game_stats = pitch_data.groupby('game_date').agg({
            'pitch_type': 'count',
            'release_speed': 'mean',
            'release_spin_rate': 'mean',
            'p_throws': 'first',
            'balls': 'sum',
            'strikes': 'sum',
            'events': lambda x: (x == 'strikeout').sum(),  # Count strikeouts using the 'events' column
            'description': lambda x: (x == 'home_run').sum()  # Count home runs using 'description'
        }).reset_index()

    # Rename columns for clarity
    game_stats.rename(columns={
        'pitch_type': 'Total Pitches',
        'release_speed': 'Avg Velocity',
        'release_spin_rate': 'Avg Spin Rate',
        'p_throws': 'Throws',
        'balls': 'Balls',
        'strikes': 'Strikes',
        'events': 'Strikeouts',
        'description': 'Home Runs Allowed'
    }, inplace=True)

    return game_stats

def compute_season_totals(game_stats):
    """
    Compute season totals for the pitcher's stats.
    """
    total_pitches = game_stats['Total Pitches'].sum()
    total_strikeouts = game_stats['Strikeouts'].sum()
    total_walks = game_stats['Balls'].sum()
    total_home_runs = game_stats['Home Runs Allowed'].sum()
    avg_velocity = game_stats['Avg Velocity'].mean().round(2)
    avg_spin_rate = game_stats['Avg Spin Rate'].mean().round(2)

    totals = {
        "Total Pitches": total_pitches,
        "Total Strikeouts": total_strikeouts,
        "Total Walks": total_walks,
        "Total Home Runs Allowed": total_home_runs,
        "Average Velocity (MPH)": avg_velocity,
        "Average Spin Rate (RPM)": avg_spin_rate
    }

    return totals

# Main Execution
if __name__ == "__main__":
    while True:
        # Input: Pitcher name and season
        first_name = input("Enter the first name of the pitcher (e.g., Gerrit): ")
        last_name = input("Enter the last name of the pitcher (e.g., Cole): ")
        season = input("Enter the MLB season (e.g., 2023): ")

        try:
            # Validate season input
            if not season.isdigit() or int(season) < 2000 or int(season) > 2023:
                raise ValueError("Please enter a valid MLB season (e.g., 2023).")

            season = int(season)

            # Fetch full-season stats
            pitcher_stats = fetch_season_stats(first_name, last_name, season)

            # Display game-by-game stats
            print("\nFull Season Game-by-Game Stats:")
            print(pitcher_stats)

            # Compute and display season totals
            season_totals = compute_season_totals(pitcher_stats)
            print("\nSeason Totals:")
            for key, value in season_totals.items():
                print(f"{key}: {value}")

            # Exit the loop if data is successfully fetched
            break

        except ValueError as e:
            print(f"Error: {e}")
            print("Please try again with valid inputs.")
