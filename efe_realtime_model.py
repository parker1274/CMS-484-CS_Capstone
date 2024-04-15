from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog, leaguegamefinder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from joblib import dump, load


def build_decision_tree_for_team(team_abbreviation):
  teams_info = teams.get_teams()
  team_id = [
      team['id'] for team in teams_info
      if team['abbreviation'] == team_abbreviation
  ][0]
  seasons = ['2021-22', '2022-23', '2023-24']
  season_ids = ['22021', '22022', '22023']

  # Initialize an empty DataFrame to concatenate data from multiple seasons
  concatenated_df_with_plus_minus = pd.DataFrame()

  for season in seasons:
    # Fetch the game logs for the team for each season
    team_game_logs = teamgamelog.TeamGameLog(
        team_id=team_id, season=season).get_data_frames()[0]
    team_games_df = team_game_logs

    # Query for games where the specified team was playing for each season
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
    games = gamefinder.get_data_frames()[0]

    # Filter for the specific season and rename column to match
    games_filtered = games[games['SEASON_ID'].isin(season_ids)].rename(
        columns={
            'GAME_ID': 'Game_ID'
        }).copy()

    # Merge PLUS_MINUS into the team dataset based on Game_ID for each season
    df_with_plus_minus = pd.merge(team_games_df,
                                  games_filtered[['Game_ID', 'PLUS_MINUS']],
                                  on='Game_ID',
                                  how='left')

    # Concatenate the data from different seasons
    if concatenated_df_with_plus_minus.empty:
      concatenated_df_with_plus_minus = df_with_plus_minus
    else:
      concatenated_df_with_plus_minus = pd.concat(
          [concatenated_df_with_plus_minus, df_with_plus_minus],
          ignore_index=True)

  # Proceed with the concatenated data
  features = concatenated_df_with_plus_minus[['FGA', 'FG3A', 'FTA', 'PF']]
  target = concatenated_df_with_plus_minus['PLUS_MINUS'].dropna()

  X_train, X_test, y_train, y_test = train_test_split(features,
                                                      target,
                                                      test_size=0.2,
                                                      random_state=42)

  tree_regressor = DecisionTreeRegressor(max_depth=10,
                                         random_state=42,
                                         min_samples_split=5,
                                         min_samples_leaf=4)
  tree_regressor.fit(X_train, y_train)

  # Save the model to a file
  dump(tree_regressor,
       f"./efe_code/models/{team_abbreviation}__{seasons}__DT_model.joblib")

  predictions = tree_regressor.predict(X_test)
  rmse = np.sqrt(mean_squared_error(y_test, predictions))
  print(
      f"Model RMSE for {team_abbreviation} over seasons {', '.join(seasons)}: {rmse}"
  )

  plt.figure(figsize=(20, 10))
  plot_tree(tree_regressor,
            filled=True,
            feature_names=features.columns,
            rounded=True,
            fontsize=12)
  plt.title(
      f"Decision Tree for {team_abbreviation} over seasons {', '.join(seasons)}"
  )
  plt.savefig(f'real_time_model_{team_abbreviation}_3_seasons.png')
  plt.close()

def build_opponent_focused_tree(opponent_abbreviation):
    teams_info = teams.get_teams()
    opponent_id = [
        team['id'] for team in teams_info
        if team['abbreviation'] == opponent_abbreviation
    ][0]
    seasons = ['2021-22', '2022-23', '2023-24']
    season_ids = ['22021', '22022', '22023']

    concatenated_df_with_plus_minus = pd.DataFrame()

    for season in seasons:
      # Fetch all games during the season using the complete season string
      gamefinder = leaguegamefinder.LeagueGameFinder(
          season_nullable=season).get_data_frames()[0]

      # Filter games based on the season, ensuring it's not the opponent's own game and the team played against the opponent
      filtered_games = gamefinder[
          (gamefinder['TEAM_ID'] != opponent_id)
          & (gamefinder['MATCHUP'].str.contains(opponent_abbreviation)) &
          (gamefinder['SEASON_ID'].isin(season_ids))].rename(
              columns={
                  'GAME_ID': 'Game_ID'
              }).copy()

      # Concatenate the data from different seasons
      if concatenated_df_with_plus_minus.empty:
        concatenated_df_with_plus_minus = filtered_games
      else:
        concatenated_df_with_plus_minus = pd.concat(
            [concatenated_df_with_plus_minus, filtered_games],
            ignore_index=True)

    features = concatenated_df_with_plus_minus[['FGA', 'FG3A', 'FTA', 'PF']]
    target = concatenated_df_with_plus_minus['PLUS_MINUS'].dropna()

    X_train, X_test, y_train, y_test = train_test_split(features,
                                                        target,
                                                        test_size=0.2,
                                                        random_state=42)

    tree_regressor = DecisionTreeRegressor(max_depth=10,
                                           random_state=42,
                                           min_samples_split=5,
                                           min_samples_leaf=4)
    tree_regressor.fit(X_train, y_train)

    dump(
        tree_regressor,
        f"./efe_code/models/Against_{opponent_abbreviation}__{seasons}__DT_model.joblib"
    )

    predictions = tree_regressor.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    print(
        f"Opponent Model RMSE against {opponent_abbreviation} over seasons {', '.join(seasons)}: {rmse}"
    )

    plt.figure(figsize=(20, 10))
    plot_tree(tree_regressor,
              filled=True,
              feature_names=features.columns,
              rounded=True,
              fontsize=12)
    plt.title(
        f"Opponent Model against {opponent_abbreviation} over seasons {', '.join(seasons)}"
    )
    plt.savefig(
        f'opponent_focused_model_{opponent_abbreviation}_3_seasons.png')
    plt.close()


# Example usage
build_decision_tree_for_team('LAL')
build_opponent_focused_tree('LAL')
