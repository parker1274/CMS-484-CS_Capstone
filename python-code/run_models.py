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
import sys
from joblib import dump, load

from data_collection.feature_avgs import feature_avgs, season_avgs
from data_collection.season_stats import all_game_stats_export

model_type = sys.argv[1]
TeamA_abbreviation = sys.argv[2]
TeamB_abbreviation = sys.argv[3]
season = sys.argv[4]
try:
    number_seasons = int(sys.argv[5])
except (ValueError, IndexError) as e:
    print(f"Error converting input to integer: {e}")
    sys.exit(1)
number_past_games = int(sys.argv[6])

# print(TeamA_abbreviation)

def run_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games):


    # print(model_type)
    # print(TeamA_abbreviation)

    # Check which model is to be created
    if (model_type == "classifier"):
        # print(f"Running a classifier model for {TeamA_abbreviation}")
        process_game_outcome_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games)
    
    elif (model_type == "regressor"):
        # print(f"Running a regressor model for {TeamA_abbreviation}")
        process_predicted_stats_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games)

    # else:
        # print("The model type entered was not found.")


def process_game_outcome_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games):

    model_path = f"/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/model_creation/{model_type}_models/{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season_DT_model.joblib"

    model = load(model_path)



    TeamA_abbreviation = TeamA_abbreviation
    TeamB_abbreviation = TeamB_abbreviation
    season = season
    number_seasons = number_seasons
    # Number of past games used to create the average stats
    number_past_games = number_past_games


    # ADD MORE SEASONS -------

    pickle_file_path = f"/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/pickle_dataframes/df_{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season.pkl"
    df = pd.read_pickle(pickle_file_path)

    df.drop(['TeamA_WL'], axis=1, inplace=True)

    # print(df)

    feature_avg_df = feature_avgs(df, number_past_games)

    # print(feature_avg_df)


    # For the input data for a game outcome prediction, perhaps input the average of their stats over a given poeriod of time.
    # For instance, get their average stats over the past 10 games and enter it and check the outcome of the game

    # If I adjust the model to include the stats of the opponent that they are playing in the game we want to predict, perhaps implememnt the same stat input process

    game_statistics = {
        'assists': 25,
        'assistsTurnoverRatio': 1.8,
        'benchPoints': 35,
        'biggestLead': 15,
        'biggestScoringRun': 12,
        'blocks': 8,
        'blocksReceived': 4,
        'fastBreakPointsAttempted': 10,
        'fastBreakPointsMade': 7,
        'fastBreakPointsPercentage': 0.7,
        'fieldGoalsAttempted': 85,
        'fieldGoalsEffectiveAdjusted': 0.55,
        'fieldGoalsMade': 45,
        'fieldGoalsPercentage': 0.529,
        'foulsOffensive': 10,
        'foulsDrawn': 20,
        'foulsPersonal': 18,
        'foulsTeam': 22,
        'foulsTechnical': 2,
        'foulsTeamTechnical': 1,
        'freeThrowsAttempted': 25,
        'freeThrowsMade': 20,
        'freeThrowsPercentage': 0.8,
        'leadChanges': 5,
        'points': 110,
        'pointsAgainst': 105,
        'pointsFastBreak': 14,
        'pointsFromTurnovers': 16,
        'pointsInThePaint': 40,
        'pointsInThePaintAttempted': 50,
        'pointsInThePaintMade': 30,
        'pointsInThePaintPercentage': 0.6,
        'pointsSecondChance': 12,
        'reboundsDefensive': 30,
        'reboundsOffensive': 15,
        'reboundsPersonal': 45,
        'reboundsTeam': 5,
        'reboundsTeamDefensive': 0,
        'reboundsTeamOffensive': 5,
        'reboundsTotal': 50,
        'secondChancePointsAttempted': 10,
        'secondChancePointsMade': 5,
        'secondChancePointsPercentage': 0.5,
        'steals': 9,
        'threePointersAttempted': 25,
        'threePointersMade': 10,
        'threePointersPercentage': 0.4,
        'timesTied': 4,
        'trueShootingAttempts': 95.5,
        'trueShootingPercentage': 0.58,
        'turnovers': 12,
        'turnoversTeam': 2,
        'turnoversTotal': 14,
        'twoPointersAttempted': 60,
        'twoPointersMade': 35,
        'twoPointersPercentage': 0.583
    }

    # input_data = pd.DataFrame([game_statistics])

    input_data = feature_avg_df

    # input_data_df = pd.DataFrame([game_statistics])

    # Assuming input_data is a pandas Series
    input_data_df = input_data.to_frame().T  # Transposes the Series to a DataFrame

    # print(f"Average data over the past {number_past_games}.")
    # print(input_data_df)


    # # Drop the columns that aren't features the model was trained on
    input_data_df.drop(['pointsAgainst_diff', 'pointsAgainst_ratio', 'points_diff', 'points_ratio'], axis=1, inplace=True)

    # print(input_data_df)


    # Make predictions and retrieve probabilities
    prediction = model.predict(input_data_df)
    probabilities = model.predict_proba(input_data_df)

    # # Output the model's prediction
    # if prediction[0] == 1:
    #     print(f"The model predicts a win for the team with a probability of {probabilities[0][1]:.2%}.")
    # else:
    #     print(f"The model predicts a loss for the team with a probability of {probabilities[0][0]:.2%}.")

    # # Display both probabilities for clarity
    # print(f"Win Probability: {probabilities[0][1]:.8%}")
    # print(f"Loss Probability: {probabilities[0][0]:.8%}")

    # print(probabilities)

    # Construct the dictionary with the relevant information
    result_data = {
        "prediction_outcome": "Win" if prediction[0] == 1 else "Loss",
        "prediction_probability": f"{probabilities[0][1]:.2%}" if prediction[0] == 1 else f"{probabilities[0][0]:.2%}",
        "probabilities": {
            "win_probability": f"{probabilities[0][1]:.8%}",
            "loss_probability": f"{probabilities[0][0]:.8%}"
        }
    }



    # Use json.dumps() to convert the dictionary to a JSON string
    # and print it so that Node.js can capture the output
    print(json.dumps(result_data))




def process_predicted_stats_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games):

    model_path = f"/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/model_creation/{model_type}_models/{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season_DT_model.joblib"

    model = load(model_path)


    TeamA_abbreviation = TeamA_abbreviation
    TeamB_abbreviation = TeamB_abbreviation
    season = season
    number_seasons = number_seasons
    # Number of past games used to create the average stats
    number_past_games = number_past_games



    pickle_file_path = f"/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/pickle_dataframes/df_{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season.pkl"
    df = pd.read_pickle(pickle_file_path)

    # df.drop(['TeamA_WL'], axis=1, inplace=True)

    # print(df)

    feature_avg_df = feature_avgs(df, number_past_games)

    input_df = feature_avg_df.to_frame().T

    input_df.drop(['assists_diff', 'points_diff', 'reboundsTotal_diff'], axis=1, inplace=True)



    print("Input avgs:")
    print(input_df)


    season_avgs(all_game_stats_export(TeamA_abbreviation, season))

    # Sample season averages for Team A and Team B
    teamA_season_stats = season_avgs(all_game_stats_export(TeamA_abbreviation, season))
    teamB_season_stats = season_avgs(all_game_stats_export(TeamB_abbreviation, season))

    # print(teamA_season_stats)

    teamA_season_stats = teamA_season_stats[['points', 'assists', 'reboundsTotal']]
    teamB_season_stats = teamB_season_stats[['points', 'assists', 'reboundsTotal']]

    # print(teamA_season_stats)



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

    print(teamA_season_stats['reboundsTotal'])
    print(teamB_season_stats['reboundsTotal'])

    # Print the scalar output for the estimated game statistics
    print(f"Game Estimated Stats:")
    print(f"Team A - Points: {estimated_teamA_points}, Assists: {estimated_teamA_assists}, Rebounds: {estimated_teamA_rebounds}")
    print(f"Team B - Points: {estimated_teamB_points}, Assists: {estimated_teamB_assists}, Rebounds: {estimated_teamB_rebounds}\n")



run_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games)


# print("Classifier Model:")
# process_user_prediction_request("classifier", "BOS", "NYK", "2023-24", 3, 15)

# print("Regressor Model:")
# process_predicted_stats_model("regressor", "BOS", "NYK", "2023-24", 3, 15)
