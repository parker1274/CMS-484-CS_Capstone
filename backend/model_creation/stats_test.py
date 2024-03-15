import pandas as pd
import numpy as np
import json
from pprint import pprint


from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt
import time
from scipy.stats import randint
import shap


import sys
# Add the directory, not the file
sys.path.append('/Users/jkran/code/school/CMS-484-CS_Capstone/backend/data_collection/')

import game_data 
import game_stats


def all_game_stats_export(team_abbreviation, season):

    # Get all the game ids for the 2022-23 season for stat collection
    game_ids = game_data.fetch_game_ids(team_abbreviation, season)

    all_game_stats_list = [ ]

    # Record start time
    start_time = time.time()


    for game in game_ids:

        game_df, combined_team_stats_df = game_stats.individual_game_stats(game)


        new_df = pd.DataFrame([game_df['homeTeam'].iloc[0]['statistics']])

        home_points = combined_team_stats_df['points'].iloc[0]
        away_points = combined_team_stats_df['points'].iloc[1]

        new_df['Home Points'] = home_points
        new_df['Away Points'] = away_points

        all_game_stats_list.append(new_df)


    all_game_stats = pd.concat(all_game_stats_list, ignore_index=True)


    print(all_game_stats)

    # Record end time
    end_time = time.time()

    print(f"Data collection Time: {end_time - start_time} seconds\n")

    # return all_game_stats

all_game_stats_export('BOS', '2022-23')