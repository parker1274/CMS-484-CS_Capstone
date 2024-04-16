import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
from joblib import dump, load
import time
import pathlib

PARENT_PATH = pathlib.Path(__file__).parent.absolute()
print("Parent Path:", PARENT_PATH)


 
from model_creation.model_functions import remove_prefix, differential_ratio_features, grid_hyperparameter
from data_collection.season_stats import multi_season_data_export
from data_collection.feature_avgs import feature_avgs


def game_outcome_model(TeamA_abbreviation, TeamB_abbreviation, season, number_seasons):


    TeamA_abbreviation = TeamA_abbreviation
    TeamB_abbreviation = TeamB_abbreviation
    season = season
    number_seasons = number_seasons



    # Record start time
    start_time = time.time()

    # df = season_stats.all_game_stats_export(team_abbreviation, season)
    TeamA = multi_season_data_export(TeamA_abbreviation, season, number_seasons, 0)

    TeamB = multi_season_data_export(TeamB_abbreviation, season, number_seasons, 1)

    # Now you can concatenate them
    combined_df = pd.concat([TeamA, TeamB], axis=1)


    feature_names = remove_prefix(TeamA)

    print("These are the combined_features:")
    print(combined_df)

    print("These are the feature_names:")
    print(feature_names)

    print("These are the column names of the combined df:")
    print(combined_df.columns)




    # Convert all the stats to differential and ration features
    df_diff_ratio = differential_ratio_features(combined_df, feature_names)






    df_diff_ratio['TeamA_WL'] = (combined_df['TeamA_points'] > combined_df['TeamB_points']).astype(int)




    features = df_diff_ratio[['assists_diff', 'assistsTurnoverRatio_diff', 'benchPoints_diff', 'biggestLead_diff', 'biggestScoringRun_diff', 'blocks_diff', 'blocksReceived_diff', 'fastBreakPointsAttempted_diff', 'fastBreakPointsMade_diff',    'fastBreakPointsPercentage_diff', 'fieldGoalsAttempted_diff', 'fieldGoalsEffectiveAdjusted_diff', 'fieldGoalsMade_diff', 'fieldGoalsPercentage_diff',
                            'foulsOffensive_diff', 'foulsDrawn_diff', 'foulsPersonal_diff', 'foulsTeam_diff', 'foulsTechnical_diff', 'foulsTeamTechnical_diff', 'freeThrowsAttempted_diff', 'freeThrowsMade_diff', 'freeThrowsPercentage_diff', 'leadChanges_diff', 'pointsFastBreak_diff', 'pointsFromTurnovers_diff', 'pointsInThePaint_diff', 'pointsInThePaintAttempted_diff', 
                            'pointsInThePaintMade_diff', 'pointsInThePaintPercentage_diff', 'pointsSecondChance_diff', 'reboundsDefensive_diff', 'reboundsOffensive_diff', 'reboundsPersonal_diff', 'reboundsTeam_diff', 'reboundsTeamDefensive_diff',    'reboundsTeamOffensive_diff', 'reboundsTotal_diff', 'secondChancePointsAttempted_diff',    'secondChancePointsMade_diff', 'secondChancePointsPercentage_diff', 
                            'steals_diff',    'threePointersAttempted_diff', 'threePointersMade_diff', 'threePointersPercentage_diff',    'timesTied_diff', 'trueShootingAttempts_diff', 'trueShootingPercentage_diff', 'turnovers_diff',    'turnoversTeam_diff', 'turnoversTotal_diff', 'twoPointersAttempted_diff', 'twoPointersMade_diff',    'twoPointersPercentage_diff',    'assists_ratio', 'assistsTurnoverRatio_ratio',
                            'benchPoints_ratio', 'biggestLead_ratio', 'biggestScoringRun_ratio',    'blocks_ratio', 'blocksReceived_ratio', 'fastBreakPointsAttempted_ratio', 'fastBreakPointsMade_ratio',    'fastBreakPointsPercentage_ratio', 'fieldGoalsAttempted_ratio', 'fieldGoalsEffectiveAdjusted_ratio',    'fieldGoalsMade_ratio', 'fieldGoalsPercentage_ratio', 'foulsOffensive_ratio', 'foulsDrawn_ratio',
                            'foulsPersonal_ratio', 'foulsTeam_ratio', 'foulsTechnical_ratio', 'foulsTeamTechnical_ratio',    'freeThrowsAttempted_ratio', 'freeThrowsMade_ratio', 'freeThrowsPercentage_ratio', 'leadChanges_ratio', 'pointsFastBreak_ratio', 'pointsFromTurnovers_ratio',    'pointsInThePaint_ratio', 'pointsInThePaintAttempted_ratio', 'pointsInThePaintMade_ratio',
                            'pointsInThePaintPercentage_ratio', 'pointsSecondChance_ratio', 'reboundsDefensive_ratio',    'reboundsOffensive_ratio', 'reboundsPersonal_ratio', 'reboundsTeam_ratio', 'reboundsTeamDefensive_ratio',    'reboundsTeamOffensive_ratio', 'reboundsTotal_ratio', 'secondChancePointsAttempted_ratio',    'secondChancePointsMade_ratio', 'secondChancePointsPercentage_ratio', 'steals_ratio',   
                            'threePointersAttempted_ratio', 'threePointersMade_ratio', 'threePointersPercentage_ratio',    'timesTied_ratio', 'trueShootingAttempts_ratio', 'trueShootingPercentage_ratio', 'turnovers_ratio',    'turnoversTeam_ratio', 'turnoversTotal_ratio', 'twoPointersAttempted_ratio', 'twoPointersMade_ratio',    'twoPointersPercentage_ratio']]

    target = df_diff_ratio['TeamA_WL']




    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Train the decision tree
    tree = DecisionTreeClassifier(max_depth=8, random_state=42)
    tree.fit(X_train, y_train)

    # Predict and evaluate
    predictions = tree.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy}\n")

    # Save the model to a file
    dump(tree, f"./model_creation/classifier_models/{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season_DT_model.joblib")



    # Visualize the decision tree
    plt.figure(figsize=(20, 10))
    plot_tree(tree, filled=True, feature_names=features.columns, class_names=['Loss', 'Win'], rounded=True, fontsize=12)

    # Extract the season from the CSV filename
    output_filename = f"./model_creation/models_png/{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season_DTC.png"

    # Save the figure with the new filename
    plt.savefig(output_filename)

    grid_hyperparameter(features, X_train, X_test, y_train, y_test)


    # Record end time
    end_time = time.time()

    print(f"Classifier model creation time: {end_time - start_time} seconds\n")





    # Evaluate model accuracy using cross-validation
    scores = cross_val_score(tree, features, target, cv=5, scoring='accuracy')

    print("Accuracy scores for each fold:", scores)
    print("Mean cross-validation accuracy:", scores.mean())









    # export_graphviz(tree, out_file='tree.dot', feature_names=['assists', 'assistsTurnoverRatio', 'benchPoints', 'biggestLead', 'biggestScoringRun', 'blocks', 'blocksReceived', 'fastBreakPointsAttempted', 'fastBreakPointsMade', 'fastBreakPointsPercentage', 'fieldGoalsAttempted', 'fieldGoalsEffectiveAdjusted', 'fieldGoalsMade', 'fieldGoalsPercentage', 'foulsOffensive', 'foulsDrawn', 'foulsPersonal', 'foulsTeam', 'foulsTechnical', 'foulsTeamTechnical', 'freeThrowsAttempted', 
    #                'freeThrowsMade', 'freeThrowsPercentage', 'leadChanges', 'points', 'pointsAgainst', 'pointsFastBreak', 'pointsFromTurnovers', 'pointsInThePaint', 'pointsInThePaintAttempted', 'pointsInThePaintMade', 'pointsInThePaintPercentage', 'pointsSecondChance', 'reboundsDefensive', 'reboundsOffensive', 'reboundsPersonal', 'reboundsTeam', 'reboundsTeamDefensive', 'reboundsTeamOffensive', 'reboundsTotal', 'secondChancePointsAttempted', 
    #                'secondChancePointsMade', 'secondChancePointsPercentage', 'steals', 'threePointersAttempted', 'threePointersMade', 'threePointersPercentage', 'timesTied', 'trueShootingAttempts', 'trueShootingPercentage', 'turnovers', 'turnoversTeam', 'turnoversTotal', 'twoPointersAttempted', 'twoPointersMade', 'twoPointersPercentage'
    # ],
    #                      class_names=['Won', 'Lost'],  filled=True, rounded=True, special_characters=True,
    #                      proportion=True)





    # print(probabilities)


    # Retrieve feature importances
    feature_importances = tree.feature_importances_

    # Match feature names with their importance scores
    features = X_train.columns
    importance_dict = dict(zip(features, feature_importances))

    # Sort features by their importance scores
    sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)

    # Unpack the feature names and their importance scores for visualization
    feature_names, importances = zip(*sorted_importance)

    # Visualize the feature importances
    plt.figure(figsize=(10, 8))
    plt.barh(feature_names, importances)
    plt.xlabel('Feature Importance Score')
    plt.ylabel('Features')
    plt.title('Feature Importances')
    plt.gca().invert_yaxis()  # Invert y-axis to have the most important feature on top
    plt.show()


    def export_df_diff_ratio(dataframe):

        dataframe.to_pickle(f"{PARENT_PATH}/pickle_dataframes/df_{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season.pkl")


    export_df_diff_ratio(df_diff_ratio)


# game_outcome_model("BOS", "NYK", "2023-24", 3)