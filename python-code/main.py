"""
Main file that will be interacted with to return predictions
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
from joblib import dump, load

model = load('/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/model_creation/classifier_models/BOS_NYK_2023-24_past_3_season_DT_model.joblib')

import sys
sys.path.append('/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/data_collection')
import feature_avgs


TeamA_abbreviation = 'BOS'
TeamB_abbreviation = 'NYK'
season = '2023-24'
number_seasons = 3
# Number of past games used to create the average stats
number_past_games = 15


# ADD MORE SEASONS -------

pickle_file_path = f"/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/pickle_dataframes/df_{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season.pkl"
df = pd.read_pickle(pickle_file_path)

df.drop(['TeamA_WL'], axis=1, inplace=True)

# print(df)

feature_avg_df = feature_avgs.feature_avgs(df, number_past_games)

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

print(f"Average data over the past {number_past_games}.")
print(input_data_df)


# # Drop the columns that aren't features the model was trained on
input_data_df.drop(['pointsAgainst_diff', 'pointsAgainst_ratio', 'points_diff', 'points_ratio'], axis=1, inplace=True)

print(input_data_df)


# Make predictions and retrieve probabilities
prediction = model.predict(input_data_df)
probabilities = model.predict_proba(input_data_df)

# Output the model's prediction
if prediction[0] == 1:
    print(f"The model predicts a win for the team with a probability of {probabilities[0][1]:.2%}.")
else:
    print(f"The model predicts a loss for the team with a probability of {probabilities[0][0]:.2%}.")

# Display both probabilities for clarity
print(f"Win Probability: {probabilities[0][1]:.8%}")
print(f"Loss Probability: {probabilities[0][0]:.8%}")

print(probabilities)

