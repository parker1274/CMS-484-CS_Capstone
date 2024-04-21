import sys
import json
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog, leaguegamefinder
import pandas as pd
from sklearn.tree import DecisionTreeRegressor, _tree
from joblib import load
import numpy as np
import os


def get_recent_games_stats(team_abbreviation,
                           number_past_games=15,
                           season='2023-24'):
    team_id = [
        team['id'] for team in teams.get_teams()
        if team['abbreviation'] == team_abbreviation
    ][0]
    team_game_logs = teamgamelog.TeamGameLog(team_id=team_id,
                                             season=season).get_data_frames()[0]
    recent_games = team_game_logs.head(number_past_games)
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
            # Define operator here based on whether we're going left ("<=") or right (">")
            if tree_.children_left[node] != _tree.TREE_LEAF:  # Has a left child
                operator = "<="
                recurse(tree_.children_left[node],
                        path_conditions + [(name, operator, threshold, depth)],
                        depth + 1)
            if tree_.children_right[node] != _tree.TREE_LEAF:  # Has a right child
                operator = ">"
                recurse(tree_.children_right[node],
                        path_conditions + [(name, operator, threshold, depth)],
                        depth + 1)
        else:
            paths.append(path_conditions)
            path_values.append(tree_.value[node].mean())

    recurse(0, [], 0)
    max_value_index = np.argmax(path_values)
    best_path_conditions = paths[max_value_index]
    best_rules = {}
    for condition in best_path_conditions:
        feature, operator, threshold, depth = condition
        if feature not in best_rules or best_rules[feature][3] > depth:
            best_rules[feature] = condition
    return list(best_rules.values())


def get_optimal_strategies(rules):
    return [{
        'feature': feature,
        'operator': operator,
        'threshold': round(threshold, 2)
    } for feature, operator, threshold, _ in rules]


def make_prediction(model_path, avg_stats):

    # print("Current Working Directory:", model_path)
    model = load(model_path)
    feature_names = avg_stats.columns.tolist()
    best_rules = extract_best_decision_rules(model, feature_names)
    return get_optimal_strategies(best_rules)


def process_controllable_model_request(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games):
    
    # with open('./efe_code/input.json', 'r') as file:
    #     data = json.load(file)
    # team_abbreviation = data['team_abbreviation']
    # opponent_abbreviation = data['opponent_abbreviation']
    # season = data['season']

    team_abbreviation = TeamA_abbreviation
    opponent_abbreviation = TeamB_abbreviation
    season = season



    model_path_team = f"./controllable_models/{team_abbreviation}_['2021-22', '2022-23', '2023-24']_DT_model.joblib"
    model_path_opponent = f"./controllable_models/Against_{opponent_abbreviation}_['2021-22', '2022-23', '2023-24']_DT_model.joblib"

    avg_stats_team = get_recent_games_stats(team_abbreviation, season=season)
    avg_stats_opponent = get_recent_games_stats(opponent_abbreviation,
                                                season=season)

    strategies_team = make_prediction(model_path_team, avg_stats_team)
    strategies_opponent = make_prediction(model_path_opponent,
                                          avg_stats_opponent)

    result_data = {
        "team_strategies": {
            "team": team_abbreviation,
            "strategies": strategies_team
        },
        "opponent_strategies": {
            "team": opponent_abbreviation,
            "strategies": strategies_opponent
        }
    }

    print(json.dumps(result_data))


# model_type = sys.argv[1]
# TeamA_abbreviation = sys.argv[2]
# TeamB_abbreviation = sys.argv[3]
# season = sys.argv[4]
# try:
#     number_seasons = int(sys.argv[5])
# except (ValueError, IndexError) as e:
#     print(f"Error converting input to integer: {e}")
#     sys.exit(1)
# number_past_games = int(sys.argv[6])

# model_type = 'controllablePrediction'
# TeamA_abbreviation = 'LAL'
# TeamB_abbreviation = 'ORL'
# season = '2023-24'
# try:
#     number_seasons = 3
# except (ValueError, IndexError) as e:
#     print(f"Error converting input to integer: {e}")
#     sys.exit(1)
# number_past_games = 15

# process_controllable_model_request(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games)