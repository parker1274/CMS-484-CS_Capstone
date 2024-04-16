"""
Main file that will take matchup specific inputs and return predictions

Will take the following inputs:
- model_type (Classifier or regressor for now, others later)
- TeamA_abbreviation (Team for the outcome we want)
- TeamB_abbreviation (Other team in the matchup)
- season (Always the current season, then goes back based on the number of season)
- number_seasons (Number of seasons we want going back for the current season)
- number_past_games (The number of recent games we want to get the average stats from for the model)
"""

import pandas as pd
import json
from joblib import load
import pathlib
import sys

from aws_lambda_powertools import Logger
from data_collection.feature_avgs import feature_avgs, season_avgs
from data_collection.season_stats import all_game_stats_export

LOGGER = Logger(level="DEBUG")
PARENT_PATH = pathlib.Path(__file__).parent.absolute()

class InvalidModelTypeError(Exception):
    pass

def run_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games):
    if (model_type == "classifier"):
        LOGGER.debug(f"Running a classifier model for {TeamA_abbreviation}")
        return process_game_outcome_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games)
    elif (model_type == "regressor"):
        LOGGER.debug(f"Running a regressor model for {TeamA_abbreviation}")
        return process_predicted_stats_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games)
    else:
        raise InvalidModelTypeError("The model type entered was not found.")


def process_game_outcome_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games):

    model_path = f"{PARENT_PATH}/model_creation/{model_type}_models/{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season_DT_model.joblib"

    model = load(model_path)

    TeamA_abbreviation = TeamA_abbreviation
    TeamB_abbreviation = TeamB_abbreviation
    season = season
    number_seasons = number_seasons
    # Number of past games used to create the average stats
    number_past_games = number_past_games

    # ADD MORE SEASONS -------
    pickle_file_path = f"{PARENT_PATH}/model_creation/pickle_dataframes/df_{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season.pkl"
    df = pd.read_pickle(pickle_file_path)
    df.drop(['TeamA_WL'], axis=1, inplace=True)

    input_data = feature_avgs(df, number_past_games)

    # Assuming input_data is a pandas Series
    input_data_df = input_data.to_frame().T  # Transposes the Series to a DataFrame

    # # Drop the columns that aren't features the model was trained on
    input_data_df.drop(['pointsAgainst_diff', 'pointsAgainst_ratio', 'points_diff', 'points_ratio'], axis=1, inplace=True)

    # Make predictions and retrieve probabilities
    prediction = model.predict(input_data_df)
    probabilities = model.predict_proba(input_data_df)

    # Output the model's prediction
    if prediction[0] == 1:
        LOGGER.debug(f"The model predicts a win for the team with a probability of {probabilities[0][1]:.2%}.")
    else:
        LOGGER.debug(f"The model predicts a loss for the team with a probability of {probabilities[0][0]:.2%}.")

    LOGGER.debug(f"Win Probability: {probabilities[0][1]:.8%}")
    LOGGER.debug(f"Loss Probability: {probabilities[0][0]:.8%}")
    LOGGER.debug(f"Probabilities: {probabilities}")

    # Construct the dictionary with the relevant information
    result_data = {
        "prediction_outcome": "Win" if prediction[0] == 1 else "Loss",
        "prediction_probability": f"{probabilities[0][1]:.2%}" if prediction[0] == 1 else f"{probabilities[0][0]:.2%}",
        "probabilities": {
            "win_probability": f"{probabilities[0][1]:.8%}",
            "loss_probability": f"{probabilities[0][0]:.8%}"
        }
    }

    return(result_data)


def process_predicted_stats_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games):

    model_path = f"{PARENT_PATH}/model_creation/{model_type}_models/{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season_DT_model.joblib"

    model = load(model_path)

    TeamA_abbreviation = TeamA_abbreviation
    TeamB_abbreviation = TeamB_abbreviation
    season = season
    number_seasons = number_seasons
    # Number of past games used to create the average stats
    number_past_games = number_past_games

    pickle_file_path = f"{PARENT_PATH}/pickle_dataframes/df_{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season.pkl"
    df = pd.read_pickle(pickle_file_path)

    # df.drop(['TeamA_WL'], axis=1, inplace=True)

    # LOGGER.debug(df)

    feature_avg_df = feature_avgs(df, number_past_games)

    input_df = feature_avg_df.to_frame().T

    input_df.drop(['assists_diff', 'points_diff', 'reboundsTotal_diff'], axis=1, inplace=True)

    LOGGER.debug(f"Input avgs: {input_df}")

    season_avgs(all_game_stats_export(TeamA_abbreviation, season))

    teamA_season_stats = season_avgs(all_game_stats_export(TeamA_abbreviation, season))
    teamB_season_stats = season_avgs(all_game_stats_export(TeamB_abbreviation, season))

    teamA_season_stats = teamA_season_stats[['points', 'assists', 'reboundsTotal']]
    teamB_season_stats = teamB_season_stats[['points', 'assists', 'reboundsTotal']]

    predictions = model.predict(input_df)
    predictions_df = pd.DataFrame(predictions, columns=['predicted_points_diff', 
                                                        'predicted_assists_diff', 'predicted_reboundsTotal_diff'])

    # Calculate the estimated game statistics based on model predictions
    # This is a simplified example; you might need to adjust it based on your actual data structure

    # Assuming 'predictions_df' contains the predicted differences for points, assists, and rebounds
    predicted_points_diff = predictions_df['predicted_points_diff'].iloc[0]
    predicted_assists_diff = predictions_df['predicted_assists_diff'].iloc[0]
    predicted_rebounds_diff = predictions_df['predicted_reboundsTotal_diff'].iloc[0]

    # Perform calculations with scalar values
    estimated_teamA_points = (teamA_season_stats['points'] + teamB_season_stats['points']) / 2 + predicted_points_diff / 2
    estimated_teamB_points = (teamA_season_stats['points'] + teamB_season_stats['points']) / 2 - predicted_points_diff / 2

    estimated_teamA_assists = (teamA_season_stats['assists'] + teamB_season_stats['assists']) / 2 + predicted_assists_diff / 2
    estimated_teamB_assists = (teamA_season_stats['assists'] + teamB_season_stats['assists']) / 2 - predicted_assists_diff / 2

    estimated_teamA_rebounds = (teamA_season_stats['reboundsTotal'] + teamB_season_stats['reboundsTotal']) / 2 + predicted_rebounds_diff / 2
    estimated_teamB_rebounds = (teamA_season_stats['reboundsTotal'] + teamB_season_stats['reboundsTotal']) / 2 - predicted_rebounds_diff / 2

    LOGGER.debug(teamA_season_stats['reboundsTotal'])
    LOGGER.debug(teamB_season_stats['reboundsTotal'])

    # LOGGER.debug the scalar output for the estimated game statistics
    LOGGER.debug(f"Game Estimated Stats:")
    LOGGER.debug(f"Team A - Points: {estimated_teamA_points}, Assists: {estimated_teamA_assists}, Rebounds: {estimated_teamA_rebounds}")
    LOGGER.debug(f"Team B - Points: {estimated_teamB_points}, Assists: {estimated_teamB_assists}, Rebounds: {estimated_teamB_rebounds}\n")
