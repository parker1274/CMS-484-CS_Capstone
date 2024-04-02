import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
from joblib import dump, load
import time

import sys
sys.path.append('/Users/jkran/code/school/CMS-484-CS_Capstone/backend/data_collection')

import season_stats
import model_functions
import feature_avgs

TeamA_abbreviation = 'BOS'
TeamB_abbreviation = 'NYK'
season = '2023-24'
number_seasons = 3



# Record start time
start_time = time.time()

# df = season_stats.all_game_stats_export(team_abbreviation, season)
TeamA = season_stats.multi_season_data_export(TeamA_abbreviation, season, number_seasons, 0)

TeamB = season_stats.multi_season_data_export(TeamB_abbreviation, season, number_seasons, 1)

# Now you can concatenate them
combined_df = pd.concat([TeamA, TeamB], axis=1)


feature_names = model_functions.remove_prefix(TeamA)

print("These are the combined_features:")
print(combined_df)

print("These are the feature_names:")
print(feature_names)

print("These are the column names of the combined df:")
print(combined_df.columns)


# Convert all the stats to differential and ration features
df_diff_ratio = model_functions.differential_ratio_features(combined_df, feature_names)




# df_diff_ratio['TeamA_WL'] = (combined_df['TeamA_points'] > combined_df['TeamB_points']).astype(int)




features = df_diff_ratio[['assists_diff', 'assistsTurnoverRatio_diff', 'benchPoints_diff', 'biggestLead_diff', 'biggestScoringRun_diff', 'blocks_diff', 'blocksReceived_diff', 'fastBreakPointsAttempted_diff', 'fastBreakPointsMade_diff',    'fastBreakPointsPercentage_diff', 'fieldGoalsAttempted_diff', 'fieldGoalsEffectiveAdjusted_diff', 'fieldGoalsMade_diff', 'fieldGoalsPercentage_diff',
                          'foulsOffensive_diff', 'foulsDrawn_diff', 'foulsPersonal_diff', 'foulsTeam_diff', 'foulsTechnical_diff', 'foulsTeamTechnical_diff', 'freeThrowsAttempted_diff', 'freeThrowsMade_diff', 'freeThrowsPercentage_diff', 'leadChanges_diff', 'pointsFastBreak_diff', 'pointsFromTurnovers_diff', 'pointsInThePaint_diff', 'pointsInThePaintAttempted_diff', 
                          'pointsInThePaintMade_diff', 'pointsInThePaintPercentage_diff', 'pointsSecondChance_diff', 'reboundsDefensive_diff', 'reboundsOffensive_diff', 'reboundsPersonal_diff', 'reboundsTeam_diff', 'reboundsTeamDefensive_diff',    'reboundsTeamOffensive_diff', 'reboundsTotal_diff', 'secondChancePointsAttempted_diff',    'secondChancePointsMade_diff', 'secondChancePointsPercentage_diff', 
                          'steals_diff',    'threePointersAttempted_diff', 'threePointersMade_diff', 'threePointersPercentage_diff',    'timesTied_diff', 'trueShootingAttempts_diff', 'trueShootingPercentage_diff', 'turnovers_diff',    'turnoversTeam_diff', 'turnoversTotal_diff', 'twoPointersAttempted_diff', 'twoPointersMade_diff',    'twoPointersPercentage_diff',    'assists_ratio', 'assistsTurnoverRatio_ratio',
                          'benchPoints_ratio', 'biggestLead_ratio', 'biggestScoringRun_ratio',    'blocks_ratio', 'blocksReceived_ratio', 'fastBreakPointsAttempted_ratio', 'fastBreakPointsMade_ratio',    'fastBreakPointsPercentage_ratio', 'fieldGoalsAttempted_ratio', 'fieldGoalsEffectiveAdjusted_ratio',    'fieldGoalsMade_ratio', 'fieldGoalsPercentage_ratio', 'foulsOffensive_ratio', 'foulsDrawn_ratio',
                          'foulsPersonal_ratio', 'foulsTeam_ratio', 'foulsTechnical_ratio', 'foulsTeamTechnical_ratio',    'freeThrowsAttempted_ratio', 'freeThrowsMade_ratio', 'freeThrowsPercentage_ratio', 'leadChanges_ratio', 'pointsFastBreak_ratio', 'pointsFromTurnovers_ratio',    'pointsInThePaint_ratio', 'pointsInThePaintAttempted_ratio', 'pointsInThePaintMade_ratio',
                          'pointsInThePaintPercentage_ratio', 'pointsSecondChance_ratio', 'reboundsDefensive_ratio',    'reboundsOffensive_ratio', 'reboundsPersonal_ratio', 'reboundsTeam_ratio', 'reboundsTeamDefensive_ratio',    'reboundsTeamOffensive_ratio', 'reboundsTotal_ratio', 'secondChancePointsAttempted_ratio',    'secondChancePointsMade_ratio', 'secondChancePointsPercentage_ratio', 'steals_ratio',   
                          'threePointersAttempted_ratio', 'threePointersMade_ratio', 'threePointersPercentage_ratio',    'timesTied_ratio', 'trueShootingAttempts_ratio', 'trueShootingPercentage_ratio', 'turnovers_ratio',    'turnoversTeam_ratio', 'turnoversTotal_ratio', 'twoPointersAttempted_ratio', 'twoPointersMade_ratio',    'twoPointersPercentage_ratio']]

target = df_diff_ratio[['points_diff', 'assists_diff', 'reboundsTotal_diff']]



from sklearn.tree import DecisionTreeRegressor

from sklearn.model_selection import train_test_split

# Define the list of target column names
target_columns = ['points_diff', 'assists_diff', 'reboundsTotal_diff']

# Correctly select columns from df_diff_ratio for target variables
selected_targets = df_diff_ratio[target_columns]

# # Check for NaN values in these columns
# print("Null values in target columns before cleaning:")
# print(selected_targets.isnull().sum())

print(selected_targets)

# Handling Null Values by removing rows with any NaN values in the target columns
df_cleaned = df_diff_ratio.dropna(subset=target_columns)

# Assuming your feature columns are all other columns except the target columns
feature_columns = [col for col in df_diff_ratio.columns if col not in target_columns]
X_cleaned = df_cleaned[feature_columns]
y_cleaned = df_cleaned[target_columns]

# Split the cleaned data into training and testing sets
X_train_clean, X_test_clean, y_train_clean, y_test_clean = train_test_split(
    X_cleaned, y_cleaned, test_size=0.2, random_state=42)

# Initialize the Decision Tree Regressor
tree_regressor = DecisionTreeRegressor(max_depth=8, random_state=42)

# Fit the Decision Tree Regressor with the cleaned training data
tree_regressor.fit(X_train_clean, y_train_clean)

# Optionally, predict on your test set and evaluate
predictions = tree_regressor.predict(X_test_clean)
# Here, you might want to evaluate your predictions, e.g., using mean_squared_error or another appropriate metric

print("Model training completed.")
# Note: Insert your own evaluation metrics according to your project's needs


# Save the model to a file
dump(tree_regressor, f"./regressor_models/{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season_DTR_model.joblib")



# Converting the predictions to a DataFrame
predictions_df = pd.DataFrame(predictions, columns=['predicted_points_diff', 
                                                    'predicted_assists_diff', 'predicted_reboundsTotal_diff'])

# Resetting the index of y_test_clean for a clean merge
y_test_clean_reset = y_test_clean.reset_index(drop=True)

# Merging the predicted values with the actual target values from the test set
comparison_df = pd.concat([y_test_clean_reset, predictions_df], axis=1)

# Now, let's print the first few rows to see the comparison
print(comparison_df)





from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Evaluate the model's performance using MAE for each target variable
for i, col in enumerate(target_columns):
    mae = mean_absolute_error(y_test_clean[col], predictions[:, i])
    print(f"MAE for {col}: {mae}")


# Record end time
end_time = time.time()

print(f"Data collection Time: {end_time - start_time} seconds\n")





# Sample season averages for Team A and Team B
teamA_season_stats = {'points': 110, 'assists': 24, 'rebounds': 43}
teamB_season_stats = {'points': 108, 'assists': 25, 'rebounds': 44}

# Calculate the estimated game statistics based on model predictions
# This is a simplified example; you might need to adjust it based on your actual data structure

# Assuming 'predictions_df' contains the predicted differences for points, assists, and rebounds
for index, row in predictions_df.iterrows():
    predicted_points_diff = row['predicted_points_diff']
    predicted_assists_diff = row['predicted_assists_diff']
    predicted_rebounds_diff = row['predicted_reboundsTotal_diff']
    
    # Estimating the game stats for Team A and Team B based on the predicted differences
    estimated_teamA_points = (teamA_season_stats['points'] + teamB_season_stats['points']) / 2 + predicted_points_diff / 2
    estimated_teamB_points = (teamA_season_stats['points'] + teamB_season_stats['points']) / 2 - predicted_points_diff / 2

    estimated_teamA_assists = (teamA_season_stats['assists'] + teamB_season_stats['assists']) / 2 + predicted_assists_diff / 2
    estimated_teamB_assists = (teamA_season_stats['assists'] + teamB_season_stats['assists']) / 2 - predicted_assists_diff / 2

    estimated_teamA_rebounds = (teamA_season_stats['rebounds'] + teamB_season_stats['rebounds']) / 2 + predicted_rebounds_diff / 2
    estimated_teamB_rebounds = (teamA_season_stats['rebounds'] + teamB_season_stats['rebounds']) / 2 - predicted_rebounds_diff / 2

    print(f"Game {index+1} Estimated Stats:")
    print(f"Team A - Points: {estimated_teamA_points}, Assists: {estimated_teamA_assists}, Rebounds: {estimated_teamA_rebounds}")
    print(f"Team B - Points: {estimated_teamB_points}, Assists: {estimated_teamB_assists}, Rebounds: {estimated_teamB_rebounds}\n")
