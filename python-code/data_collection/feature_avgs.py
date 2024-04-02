"""
Calculate the averages of features
"""

import pandas as pd
import season_gen_data



# def feature_avgs_past_5_games()


def feature_avgs(game_dataframe, num_previous_games):

    df = game_dataframe

    selected_games_df = df.iloc[:num_previous_games]

    # print(selected_games_df)


    average_values_df = selected_games_df.select_dtypes(include=['number']).mean()


    return average_values_df

