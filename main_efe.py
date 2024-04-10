"""
Main file that will be interacted with to return predictions
"""

from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog, leaguegamefinder
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
from joblib import dump, load


def get_recent_games_stats(team_abbreviation,
                           number_past_games=15,
                           season='2023-24'):
  team_id = [
      team['id'] for team in teams.get_teams()
      if team['abbreviation'] == team_abbreviation
  ][0]
  team_game_logs = teamgamelog.TeamGameLog(team_id=team_id,
                                           season=season).get_data_frames()[0]

  # Assuming the DataFrame is sorted in descending order by date, if not, sort it
  recent_games = team_game_logs.head(number_past_games)

  # print(recent_games)

  # Calculate the average stats for the recent games
  avg_stats = recent_games[['FGA', 'FG3A', 'FTA', 'PF']].mean().to_frame().T
  return avg_stats


def make_prediction(model_path, avg_stats):
  model = load(model_path)
  prediction = model.predict(avg_stats)

  # Get feature importances
  feature_importances = model.feature_importances_

  # Get the names of the features from avg_stats
  feature_names = avg_stats.columns

  # Combine feature names and their importance scores
  feature_importance_dict = dict(zip(feature_names, feature_importances))

  # Sort the features by importance
  sorted_feature_importance = sorted(feature_importance_dict.items(),
                                     key=lambda x: x[1],
                                     reverse=True)

  print("Feature importances:")
  for feature, importance in sorted_feature_importance:
    print(f"{feature}: {importance:.4f}")

  return prediction


# Example usage for both the team and its opponent
team_abbreviation = 'ORL'
opponent_abbreviation = 'LAL'
season = '2023-24'
model_path_team = f"./efe_code/models/{team_abbreviation}__['2021-22', '2022-23', '2023-24']__DT_model.joblib"
model_path_opponent = f"./efe_code/models/Against_{opponent_abbreviation}__['2021-22', '2022-23', '2023-24']__DT_model.joblib"

avg_stats_team = get_recent_games_stats(team_abbreviation, season=season)
avg_stats_opponent = get_recent_games_stats(opponent_abbreviation,
                                            season=season)

prediction_team = make_prediction(model_path_team, avg_stats_team)
prediction_opponent = make_prediction(model_path_opponent, avg_stats_opponent)

print(
    f"Prediction for {team_abbreviation} using the team-focused model: {prediction_team}"
)
print(
    f"Prediction against {opponent_abbreviation} using the opponent-focused model: {prediction_opponent}"
)
