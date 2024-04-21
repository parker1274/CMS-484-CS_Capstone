import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt
import time
from scipy.stats import randint
import shap




def grid_hyperparameter(feature_names, X_train, X_test, y_train, y_test):

    # Define the parameter grid to search over
    param_grid = {
        'criterion': ['gini', 'entropy'],
        'max_depth': [10, 15, 20],  # Introduced maximum depths
        'min_samples_split': [4, 6, 8],  # Increased minimum samples to split
        'min_samples_leaf': [2, 3, 4],  # Increased minimum samples per leaf
        'max_features': ['sqrt', 'log2'],  # Consider sqrt and log2 of features at each split
    }

    
    # Initialize the GridSearchCV object
    grid_search = GridSearchCV(DecisionTreeClassifier(random_state=42), param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=1)
    grid_search.fit(X_train, y_train)
    
    # Best model parameters and score
    best_tree = grid_search.best_estimator_
    print("Best parameters:", grid_search.best_params_)
    print(f"Best score: {grid_search.best_score_}\n")

    # Evaluate the best model on the test set
    start_time = time.time()
    predictions = best_tree.predict(X_test)
    end_time = time.time()

    # Calculate metrics
    new_accuracy = accuracy_score(y_test, predictions)
    new_precision = precision_score(y_test, predictions, average='binary')
    new_recall = recall_score(y_test, predictions, average='binary')
    new_f1 = f1_score(y_test, predictions, average='binary')

    print(f"Grid Search Performance:\nAccuracy: {new_accuracy}\nPrecision: {new_precision}\nRecall: {new_recall}\nF1 Score: {new_f1}")
    print(f"Training and Prediction Time: {end_time - start_time} seconds")

    # Before the plot_tree line, ensure feature_names is correctly defined:
    feature_names = list(X_train.columns)  # Assuming X_train is a DataFrame with the correct columns

    # Then, when calling plot_tree, you can use:
    plot_tree(best_tree, filled=True, feature_names=feature_names, class_names=['Loss', 'Win'], rounded=True, fontsize=12)

    
    # # Visualize the decision tree
    # plt.figure(figsize=(20, 10))
    # plot_tree(best_tree, filled=True, feature_names=feature_names, class_names=['Loss', 'Win'], rounded=True, fontsize=12)
    # plt.show()

    return best_tree



def differential_ratio_features(combined_df, features_df):

    # print("These are the combined_features:")
    # print(combined_df)
    # print("These are the features:")
    # print(features_df)

       
    # Drop the columns that can't be used in the model
    combined_df.drop(['TeamA_BOS', 'TeamA_Opponent', 'TeamA_WL', 'TeamA_biggestLeadScore', 'TeamA_biggestScoringRunScore', 'TeamA_minutes', 'TeamA_minutesCalculated', 'TeamA_timeLeading',
             'TeamB_NYK', 'TeamB_Opponent', 'TeamB_WL', 'TeamB_biggestLeadScore', 'TeamB_biggestScoringRunScore', 'TeamB_minutes', 'TeamB_minutesCalculated', 'TeamB_timeLeading'], 
             axis=1, inplace=True)
    
    
    # Drop the same columns from the feature list
    features_df.drop(['BOS', 'WL', 'Opponent', 'biggestLeadScore', 'biggestScoringRunScore', 'minutes', 'minutesCalculated', 'timeLeading'],
                     axis=1, inplace=True)


    
    # Initialize DataFrames to hold differential and ratio features
    df_diff = pd.DataFrame(index=combined_df.index)
    df_ratio = pd.DataFrame(index=combined_df.index)

    # Iterate over the column names in features_df to generate differential and ratio features
    for feature in features_df.columns:
        diff_col_name = f"{feature}_diff"
        ratio_col_name = f"{feature}_ratio"
        
        # Calculate differential and ratio values
        diff_values = combined_df[f'TeamA_{feature}'] - combined_df[f'TeamB_{feature}']
        ratio_values = combined_df[f'TeamA_{feature}'] / (combined_df[f'TeamB_{feature}'] + np.finfo(float).eps)  # Adding epsilon to avoid division by zero
        
        # Store the calculated values in the respective DataFrames
        df_diff[diff_col_name] = diff_values
        df_ratio[ratio_col_name] = ratio_values

    
    df_diff_ratio = pd.concat([df_diff, df_ratio], axis=1)

    df_diff_ratio['TeamA_WL'] = (df_diff_ratio['points_diff'] > 0).astype(int)

    # # Calculate the season-wide average of differential and ratio features
    # average_features_df = df_diff_ratio.mean().to_frame().T
    # average_features_df.index = ['season_average']

    # # Output the average features for review
    # print(average_features_df)

    print(df_diff_ratio.columns)

    return df_diff_ratio



def remove_prefix(dataframe):

    df = dataframe

    # Prefix to remove
    prefix_to_remove = 'TeamA_'

    # Remove the prefix from all column names
    df.columns = [col.replace(prefix_to_remove, '') for col in df.columns]

    return df
