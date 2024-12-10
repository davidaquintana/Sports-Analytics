import nfl_data_py as nfl
import pandas as pd
import matplotlib.pyplot as plt

# Fetch game-by-game stats for a given season
def fetch_game_stats(season, qb_name):
    """
    Fetch game-by-game stats for the specified season and quarterback.
    """
    print(f"Fetching stats for {qb_name} in season {season}...")

    # Import weekly data
    game_stats = nfl.import_weekly_data([season])

    # Filter stats for the specified quarterback
    qb_game_stats = game_stats[game_stats['player_display_name'] == qb_name]

    if qb_game_stats.empty:
        raise ValueError(f"No data found for {qb_name} in season {season}.")

    return qb_game_stats

# Add custom metrics
def compute_advanced_metrics(qb_game_stats):
    """
    Compute advanced metrics for the quarterback's game stats.
    """
    # Use the correct column names based on the dataset
    required_columns = ['completions', 'attempts', 'passing_yards', 'passing_tds', 'interceptions']
    missing_columns = [col for col in required_columns if col not in qb_game_stats.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    qb_game_stats['Completion%'] = (
        qb_game_stats['completions'] / qb_game_stats['attempts'] * 100
    ).round(2)
    qb_game_stats['Yards per Attempt'] = (
        qb_game_stats['passing_yards'] / qb_game_stats['attempts']
    ).round(2)
    qb_game_stats['TD-INT Ratio'] = (
        qb_game_stats['passing_tds'] / qb_game_stats['interceptions'].replace(0, 1)
    ).round(2)  # Avoid division by zero
    return qb_game_stats

# Compute season totals
def compute_season_totals(qb_game_stats):
    """
    Compute season totals for key metrics.
    """
    total_completions = qb_game_stats['completions'].sum()
    total_attempts = qb_game_stats['attempts'].sum()
    total_yards = qb_game_stats['passing_yards'].sum()
    total_tds = qb_game_stats['passing_tds'].sum()
    total_ints = qb_game_stats['interceptions'].sum()
    completion_percentage = (total_completions / total_attempts * 100).round(2) if total_attempts > 0 else 0
    yards_per_attempt = (total_yards / total_attempts).round(2) if total_attempts > 0 else 0
    td_int_ratio = (total_tds / total_ints).round(2) if total_ints > 0 else total_tds

    totals = {
        "Total Completions": total_completions,
        "Total Attempts": total_attempts,
        "Total Passing Yards": total_yards,
        "Total Passing TDs": total_tds,
        "Total Interceptions": total_ints,
        "Completion%": completion_percentage,
        "Yards per Attempt": yards_per_attempt,
        "TD-INT Ratio": td_int_ratio,
    }

    return totals

# Main Execution
if __name__ == "__main__":
    while True:
        # Input: QB name and season
        qb_name = input("Enter the name of the quarterback (e.g., Patrick Mahomes): ")
        season = input("Enter the NFL season (e.g., 2023): ")

        try:
            # Validate season input
            if not season.isdigit() or int(season) < 2000 or int(season) > 2023:
                raise ValueError("Please enter a valid NFL season (e.g., 2023).")

            season = int(season)

            # Step 1: Fetch game-by-game stats
            qb_game_stats = fetch_game_stats(season, qb_name)

            # Step 2: Compute advanced metrics
            qb_game_stats = compute_advanced_metrics(qb_game_stats)

            # Step 3: Display week-by-week stats
            print("\nGame-by-Game Stats with Advanced Metrics:")
            print(qb_game_stats[['week', 'opponent_team', 'passing_yards', 'passing_tds', 'interceptions', 
                                 'Completion%', 'Yards per Attempt', 'TD-INT Ratio']])

            # Step 4: Compute and display season totals
            totals = compute_season_totals(qb_game_stats)
            print("\nSeason Totals:")
            for key, value in totals.items():
                print(f"{key}: {value}")

            # Exit the loop if data is successfully fetched
            break

        except ValueError as e:
            print(f"Error: {e}")
            print("Please try again with a valid NFL quarterback and season.")
