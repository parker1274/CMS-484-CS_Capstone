"""
File for creating the models

Will take the following inputs:
- model_type (Classifier or regressor for now, others later)
- TeamA_abbreviation (Team for the outcome we want)
- TeamB_abbreviation (Other team in the matchup)
- season (Always the current season, then goes back based on the number of season)
- number_seasons (Number of seasons we want going back for the current season)
- number_past_games (The number of recent games we want to get the average stats from for the model)
"""

from model_creation.decision_tree_model import game_outcome_model
from model_creation.multi_stat_model import predicted_stats_model






def create_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons):

    print(model_type)
    print(TeamA_abbreviation)

    # Check which model is to be created
    if (model_type == "classifier"):
        print(f"Creating a classifier model for {TeamA_abbreviation}")
        game_outcome_model(TeamA_abbreviation, TeamB_abbreviation, season, number_seasons)
    
    elif (model_type == "regressor"):
        print(f"Creating a regressor model for {TeamA_abbreviation}")
        predicted_stats_model(TeamA_abbreviation, TeamB_abbreviation, season, number_seasons)

    else:
        print("The model type entered was not found.")

# create_model("classifier", "BOS", "NYK", "2023-24", 3)