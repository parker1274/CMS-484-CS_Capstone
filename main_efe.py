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
import numpy as np
from sklearn.tree import _tree


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


def extract_best_decision_rules(tree, feature_names):
  tree_ = tree.tree_
  feature_name = [
      feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined!"
      for i in tree_.feature
  ]
  paths = []
  path_values = []

  def recurse(node, path_conditions, depth):
    if tree_.feature[node] != _tree.TREE_UNDEFINED:
      name = feature_name[node]
      threshold = tree_.threshold[node]
      left_subpath = path_conditions + [(name, "<=", threshold, depth)]
      right_subpath = path_conditions + [(name, ">", threshold, depth)]
      recurse(tree_.children_left[node], left_subpath, depth + 1)
      recurse(tree_.children_right[node], right_subpath, depth + 1)
    else:
      # Node is a leaf
      paths.append(path_conditions)
      path_values.append(tree_.value[node].mean())

  recurse(0, [], 0)

  # Extract paths that lead to the best outcomes
  max_value_index = np.argmax(path_values)
  best_path_conditions = paths[max_value_index]
  # Filter to keep only the most impactful rule per feature
  best_rules = {}
  for condition in best_path_conditions:
    feature, operator, threshold, depth = condition
    if feature not in best_rules or best_rules[feature][3] > depth:
      best_rules[feature] = condition
  return list(best_rules.values())


def print_optimal_ranges(rules, team_abbreviation, context="for"):

  if context == "for":
    print(f"Optimal Game Strategies for {team_abbreviation}:")
  else:
    print(f"Optimal Game Strategies against {team_abbreviation}:")

  features = []
  operators = []
  thresholds = []
  for feature, operator, threshold, depth in sorted(rules, key=lambda x: x[3]):
    features.append(feature)
    operators.append(operator)
    thresholds.append(threshold)

  # print(f" - {feature} {operator} {threshold:.2f}")

  print(features)
  print(operators)
  print(thresholds)


def make_prediction(model_path, avg_stats, team_abbreviation, context="for"):
  model = load(model_path)
  prediction = model.predict(avg_stats)

  # Get the names of the features from avg_stats
  feature_names = avg_stats.columns.tolist()

  # Extract best decision rules
  best_rules = extract_best_decision_rules(model, feature_names)
  print_optimal_ranges(best_rules, team_abbreviation, context)

  return prediction


# Example usage for both the team and its opponent
team_abbreviation = 'LAL'
opponent_abbreviation = 'ORL'
season = '2023-24'
model_path_team = f"./efe_code/models/{team_abbreviation}__['2021-22', '2022-23', '2023-24']__DT_model.joblib"
model_path_opponent = f"./efe_code/models/Against_{opponent_abbreviation}__['2021-22', '2022-23', '2023-24']__DT_model.joblib"

avg_stats_team = get_recent_games_stats(team_abbreviation, season=season)
avg_stats_opponent = get_recent_games_stats(opponent_abbreviation,
                                            season=season)

prediction_team = make_prediction(model_path_team, avg_stats_team,
                                  team_abbreviation, "for")
prediction_opponent = make_prediction(model_path_opponent, avg_stats_opponent,
                                      opponent_abbreviation, "against")

print(
    f"Prediction for {team_abbreviation} using the team-focused model: {prediction_team}"
)
print(
    f"Prediction against {opponent_abbreviation} using the opponent-focused model: {prediction_opponent}"
)
