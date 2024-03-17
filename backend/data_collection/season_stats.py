import pandas as pd
import numpy as np
import json
from pprint import pprint



import matplotlib.pyplot as plt
import time
from scipy.stats import randint
import shap

import season_gen_data 
import game_stats







def all_game_stats_export(team_abbreviation, season):

    # Get all the game ids for the 2022-23 season for stat collection
    game_ids = season_gen_data.fetch_game_ids(team_abbreviation, season)

    all_game_stats_list = [ ]

    # Record start time
    start_time = time.time()


    for game in game_ids:

        game_df = game_stats.individual_game_stats(game)

        # Check if the selected team is home or away
        if game_df['homeTeam'].iloc[0]['teamTricode'] == team_abbreviation:
            new_df = pd.DataFrame([game_df['homeTeam'].iloc[0]['statistics']])
            selected_team = game_df['homeTeam'].iloc[0]['score']
            opp_team = game_df['awayTeam'].iloc[0]['score']
            # opp_abbreviation = game_df['awayTeam'].iloc[0]['teamTricode']

        else:
            new_df = pd.DataFrame([game_df['awayTeam'].iloc[0]['statistics']])
            opp_team = game_df['homeTeam'].iloc[0]['score']
            selected_team = game_df['awayTeam'].iloc[0]['score']
            # opp_abbreviation = game_df['homeTeam'].iloc[0]['teamTricode']




        new_df[f"{team_abbreviation}"] = selected_team
        new_df['Opppnent'] = opp_team

        if selected_team > opp_team:
            outcome = 1
        else:
            outcome = 0

        new_df['WL'] = outcome

        all_game_stats_list.append(new_df)


    all_game_stats = pd.concat(all_game_stats_list, ignore_index=True)


    pprint(all_game_stats)

    # Record end time
    end_time = time.time()

    print(f"Data collection Time: {end_time - start_time} seconds\n")

    return all_game_stats

# data = all_game_stats_export('BOS','2023-24')

# data.to_csv('testfile.csv')