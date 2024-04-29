import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
from joblib import dump, load
import time

import sys
sys.path.append('/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/data_collection')

 
from model_creation.model_functions import remove_prefix, differential_ratio_features, differential_ratio_stats, grid_hyperparameter
from data_collection.season_stats import multi_season_data_export
from data_collection.feature_avgs import feature_avgs


def game_outcome_model(TeamA_abbreviation, TeamB_abbreviation, season, number_seasons):


    TeamA_abbreviation = TeamA_abbreviation
    TeamB_abbreviation = TeamB_abbreviation
    season = season
    number_seasons = number_seasons
    TeamA_identifier = 0
    TeamB_identifier = 1



    # Record start time
    start_time = time.time()

    # df = season_stats.all_game_stats_export(team_abbreviation, season)
    TeamA_df = multi_season_data_export(TeamA_abbreviation, season, number_seasons, TeamA_identifier)
    print(list(TeamA_df.columns))

    TeamA_df.drop

    

    # Select columns that start with 'sales'
    selected_names = remove_prefix(TeamA_df, 'TeamA_')
    # print(list(TeamA_df.columns))

    # print("Selected")
    # print(list(selected_names.columns))

    cols_to_select = selected_names.columns.str.startswith('Selected_')
    selected_columns = selected_names.loc[:, cols_to_select]
    feature_df = remove_prefix(selected_columns, 'Selected_')


    # print("Features")
    # print(list(feature_df.columns))

    TeamB_df = multi_season_data_export(TeamB_abbreviation, season, number_seasons, TeamB_identifier)
    # print(list(TeamB_df.columns))






    print("Team A differential df")
    TeamA_diff_ratio_df = differential_ratio_stats(TeamA_df, feature_df, TeamA_abbreviation, TeamA_identifier)
    print(TeamA_diff_ratio_df)

    print("Team B differential df")
    TeamB_diff_ratio_df = differential_ratio_stats(TeamB_df, feature_df, TeamB_abbreviation, TeamB_identifier)
    print(TeamB_diff_ratio_df)



    # Now you can concatenate them
    combined_df = pd.concat([TeamA_diff_ratio_df, TeamB_diff_ratio_df], axis=1)




    # feature_names = remove_prefix(TeamA)

    print("These are the combined_features:")
    print(combined_df)

    # print("These are the feature_names:")
    # print(feature_names)

    # print("These are the column names of the combined df:")
    # print(combined_df.columns)




    # # Convert all the stats to differential and ration features
    # df_diff_ratio = differential_ratio_features(combined_df, feature_names, TeamA_abbreviation, TeamB_abbreviation)

    all_columns = combined_df.columns.tolist()
    print(all_columns)





    # df_diff_ratio['TeamA_WL'] = (combined_df['TeamA_points'] > combined_df['TeamB_points']).astype(int)

    combined_df.drop(['TeamA_points_ratio', 'TeamB_points_ratio','TeamA_points_diff', 'TeamB_points_diff',
                      'TeamA_pointsAgainst_diff','TeamB_pointsAgainst_diff', 
                      'TeamA_pointsAgainst_ratio','TeamB_pointsAgainst_ratio',
                      'TeamA_fieldGoalsEffectiveAdjusted_diff','TeamB_fieldGoalsEffectiveAdjusted_diff',
                      'TeamA_fieldGoalsEffectiveAdjusted_ratio','TeamB_fieldGoalsEffectiveAdjusted_ratio',
                      'TeamA_trueShootingPercentage_ratio', 'TeamB_trueShootingPercentage_ratio',
                      'TeamA_trueShootingPercentage_diff', 'TeamB_trueShootingPercentage_diff'], axis=1, inplace=True)

    # Get column names from each DataFrame
    all_columns = combined_df.columns.tolist()

    all_columns.remove('TeamA_Selected_WL')

    print(all_columns)


    features = combined_df[all_columns]
    target = combined_df['TeamA_Selected_WL']




    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.1, random_state=42)

    # Train the decision tree
    tree = DecisionTreeClassifier(max_depth=8, random_state=42)
    tree.fit(X_train, y_train)

    print()
    print("new threshold")
    probabilities = tree.predict_proba(X_test)[:, 1]

    # Define a new threshold
    new_threshold = 0.5  # Lowering the threshold to classify more items as positive

    # Apply the threshold
    predictions = (probabilities > new_threshold).astype(int)


    # Predict and evaluate
    # predictions = tree.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy}\n")

    # # Save the model to a file
    # dump(tree, f"./model_creation/classifier_models/NEW_{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season_DT_model.joblib")



    # Visualize the decision tree
    plt.figure(figsize=(20, 10))
    plot_tree(tree, filled=True, feature_names=features.columns, class_names=['Loss', 'Win'], rounded=True, fontsize=12)

    # Extract the season from the CSV filename
    output_filename = f"./model_creation/models_png/{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season_DTC.png"

    # Save the figure with the new filename
    plt.savefig(output_filename)

    bestTree = grid_hyperparameter(features, X_train, X_test, y_train, y_test)
    
    # Save the model to a file
    dump(bestTree, f"./model_creation/classifier_models/NEW_{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season_DT_model.joblib")

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


    # # Retrieve feature importances
    # feature_importances = tree.feature_importances_

    # # Match feature names with their importance scores
    # features = X_train.columns
    # importance_dict = dict(zip(features, feature_importances))

    # # Sort features by their importance scores
    # sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)

    # # Unpack the feature names and their importance scores for visualization
    # feature_names, importances = zip(*sorted_importance)

    # # Visualize the feature importances
    # plt.figure(figsize=(10, 8))
    # plt.barh(feature_names, importances)
    # plt.xlabel('Feature Importance Score')
    # plt.ylabel('Features')
    # plt.title('Feature Importances')
    # plt.gca().invert_yaxis()  # Invert y-axis to have the most important feature on top
    # plt.show()


    # df_for_avgs = pd.concat([TeamA_df, TeamB_df], axis=1)


    def export_df_diff_ratio(dataframe):

        dataframe.to_pickle(f"/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/pickle_dataframes/NEW_df_{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season.pkl")


    export_df_diff_ratio(combined_df)


# game_outcome_model("BOS", "NYK", "2023-24", 3)