import pandas as pd

import matplotlib.pyplot as plt
import time
from scipy.stats import randint
import shap

from season_gen_data import fetch_game_ids
from game_stats import individual_game_stats







def all_game_stats_export(team_abbreviation, season):

    # Get all the game ids for the 2022-23 season for stat collection
    game_ids = fetch_game_ids(team_abbreviation, season)

    all_game_stats_list = [ ]

    # Record start time
    start_time = time.time()


    for game in game_ids:

        game_df = individual_game_stats(game)

        # Check if the selected team is home or away
        if game_df['homeTeam'].iloc[0]['teamTricode'] == team_abbreviation:
            selected_team_df = pd.DataFrame([game_df['homeTeam'].iloc[0]['statistics']])
            selected_team = game_df['homeTeam'].iloc[0]['score']
            opp_team = game_df['awayTeam'].iloc[0]['score']
            # opp_abbreviation = game_df['awayTeam'].iloc[0]['teamTricode']

            opponent_team_df = pd.DataFrame([game_df['awayTeam'].iloc[0]['statistics']])



            selected_team_df = selected_team_df.add_prefix('Selected_')
            opponent_team_df = opponent_team_df.add_prefix('Opponent_')


        else:
            selected_team_df = pd.DataFrame([game_df['awayTeam'].iloc[0]['statistics']])
            opp_team = game_df['homeTeam'].iloc[0]['score']
            selected_team = game_df['awayTeam'].iloc[0]['score']
            # opp_abbreviation = game_df['homeTeam'].iloc[0]['teamTricode']

            opponent_team_df = pd.DataFrame([game_df['homeTeam'].iloc[0]['statistics']])

            selected_team_df = selected_team_df.add_prefix('Selected_')
            opponent_team_df = opponent_team_df.add_prefix('Opponent_')
            

        # Concatenate the dataframes horizontally
        combined_df = pd.concat([selected_team_df, opponent_team_df], axis=1)



        combined_df[f"{team_abbreviation}"] = selected_team
        combined_df['Opponent'] = opp_team

        if selected_team > opp_team:
            outcome = 1
        else:
            outcome = 0

        combined_df['WL'] = outcome

        all_game_stats_list.append(combined_df)


    all_game_stats = pd.concat(all_game_stats_list, ignore_index=True)


    # pprint(all_game_stats)

    # Record end time
    end_time = time.time()

    # print(f"Data collection Time: {end_time - start_time} seconds\n")

    

    return all_game_stats

# data = all_game_stats_export('BOS','2023-24')

# data.to_csv('testfile.csv')


# Function to gather the complete season data for multiple seasons
# Always starts with the current season and goes backwards
def multi_season_data_export(team_abbreviation, season, num_seasons, team_identifer):

    year_str = season
    first_year = int(year_str.split('-')[0])

    # Generate the previous 5 seasons in "YYYY-YY" format
    previous_seasons = [f"{first_year - i}-{str(first_year - i + 1)[2:]}" for i in range(0, num_seasons)]

    print(previous_seasons)



    mulit_season_list = []

    # Loop through all the seasons
    for i in previous_seasons:

        # Store the season data in a temporary DF
        current_DF = all_game_stats_export(team_abbreviation, season)

        # Append the temporary DF to the holding list
        mulit_season_list.append(current_DF)

    # Convert the list of the data for each season into a DF
    multi_season_DF = pd.concat(mulit_season_list, ignore_index=True)

    # Says whether or not the selected team is the main or opponent
    # 0 for main and 1 for opp
    team_identifer = team_identifer

    if team_identifer == 0:
        # Add 'TeamA_' prefix to each column name using .add_prefix()
        multi_season_DF = multi_season_DF.add_prefix('TeamA_')
    else:
        # Add 'TeamB_' prefix to each column name using .add_prefix()
        multi_season_DF = multi_season_DF.add_prefix('TeamB_')




    # Return the final multi season DF
    return multi_season_DF


# test = all_game_stats_export('BOS', '2023-24')

# # Convert the columns object to a list and print it
# column_names = list(test.columns)
# print(column_names)

# test = multi_season_data_export('NYK', '2023-24', 3, 1)

# print(test)

# # Shape of the DataFrame
# print("Shape of DataFrame:", test.shape)

