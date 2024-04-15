from nba_api.stats.static import teams
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder
pd.set_option('display.max_columns', None)

nba_teams = teams.get_teams()
abbr = input("Enter the NBA team abbreviation: ")
season_year = input("Enter the season year (e.g., 2023): ")

# Select the dictionary for the specified team, which contains their team ID
user_team = [team for team in nba_teams if team['abbreviation'] == abbr][0]
team_id = user_team['id']

# Query for games where the specified team was playing
gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
games = gamefinder.get_data_frames()[0]

# Format the season input to match the NBA API season format (e.g., '22024' for the 2023-2024 regular season)
season_input = '2' + season_year
# Filter the games DataFrame for the specified season
filtered_games = games[games['SEASON_ID'] == season_input]
print(filtered_games)
scoring_columns = ['GAME_DATE', 'GAME_ID', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF' ]
scoring_stats = filtered_games[scoring_columns]


scoring_stats['Team_Efficiency'] = (
    scoring_stats['PTS'] +
    0.4 * scoring_stats['FGM'] -
    0.7 * (scoring_stats['FGA'] - scoring_stats['FGM']) +
    0.7 * scoring_stats['FTM'] -
    0.4 * (scoring_stats['FTA'] - scoring_stats['FTM']) +
    0.7 * scoring_stats['OREB'] +
    0.3 * scoring_stats['DREB'] +
    scoring_stats['STL'] +
    0.7 * scoring_stats['AST'] +
    0.7 * scoring_stats['BLK'] -
    scoring_stats['PF'] -
    scoring_stats['TOV']
)

print(scoring_stats.head())
games.groupby(games.SEASON_ID.str[-5:])[['GAME_ID']].count().loc['2023':]

games.head()
scoring_stats.to_pickle(f'/Users/augustalexander/Navigator PER adjusted/dr_{abbr}_{season_year}.csv')
#games.to_csv('/Users/augustalexander/Navigator PER adjusted/game.csv')
#games.to_pickle("/Users/augustalexander/Navigator PER adjusted/df_{team_id}_{season_id}.pkl")
#print(games)
