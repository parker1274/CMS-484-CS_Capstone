import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from nba_api.live.nba.endpoints import boxscore

# Function to save dictionary as JSON
def save_dict_as_json(data, filename):
    # Check if the filename ends with .json; if not, append it
    if not filename.endswith('.json'):
        filename += '.json'
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def individual_game_stats(game_id):

    # Get BoxScore
    box = boxscore.BoxScore(game_id)

    # Convert dictionaries to DataFrames
    game_df = pd.DataFrame([box.game.get_dict()])
    arena_df = pd.DataFrame([box.arena.get_dict()])
    away_team_df = pd.DataFrame([box.away_team.get_dict()])
    away_team_player_stats_df = pd.DataFrame(box.away_team_player_stats.get_dict())
    away_team_stats = pd.DataFrame([box.away_team_stats.get_dict()])  # Assuming this returns a dict with the stats
    home_team_df = pd.DataFrame([box.home_team.get_dict()])
    home_team_player_stats_df = pd.DataFrame(box.home_team_player_stats.get_dict())
    home_team_stats = pd.DataFrame([box.home_team_stats.get_dict()])  # Assuming this returns a dict with the stats

    # Assuming 'points' is a key in the team stats dictionary
    away_team_points = away_team_stats['score'].iloc[0]  # Extract points for away team
    home_team_points = home_team_stats['score'].iloc[0]  # Extract points for home team

    # Create a DataFrame for combined team stats
    combined_team_stats_df = pd.DataFrame({
        'team': ['Home', 'Away'],
        'points': [home_team_points, away_team_points]
    })


    # Nested dictionary for quick lookups
    game_data = {
        'game': box.game.get_dict(),
        'arena': box.arena.get_dict(),
        'away_team': box.away_team.get_dict(),
        'away_team_player_stats': box.away_team_player_stats.get_dict(),
        'home_team': box.home_team.get_dict(),
        'home_team_player_stats': box.home_team_player_stats.get_dict()
    }



    return game_df, combined_team_stats_df



# save_dict_as_json(game_data, 'game_stats1')

# data_for_export = {
#     "game_df": game_df,
#     "arena_df": arena_df,
#     "away_team_df": away_team_df,
#     "away_team_player_stats_df": away_team_player_stats_df,
#     "away_team_stats": away_team_stats,
#     "home_team_df": home_team_df,
#     "home_team_player_stats_df": home_team_player_stats_df,
#     "home_team_stats": home_team_stats
# }

# pd.to_pickle(data_for_export, "all_data.pkl")

# print(data_for_export)