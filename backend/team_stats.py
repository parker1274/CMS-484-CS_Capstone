# team_stats.py
import sys
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
pd.set_option('display.max_columns', None)

def fetch_and_process_data(abbr, season_year):
    nba_teams = teams.get_teams()
    user_team = [team for team in nba_teams if team['abbreviation'] == abbr][0]
    team_id = user_team['id']

    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
    games = gamefinder.get_data_frames()[0]

    season_input = '2' + season_year
    filtered_games = games[games['SEASON_ID'] == season_input]

    filtered_games['Team_Efficiency'] = (
        filtered_games['PTS'] +
        1.2 * filtered_games['FG3M'] +
        0.8 * (filtered_games['FGM'] - filtered_games['FG3M']) -
        0.7 * (filtered_games['FGA'] - filtered_games['FGM']) +
        0.7 * filtered_games['FTM'] -
        0.4 * (filtered_games['FTA'] - filtered_games['FTM']) +
        0.7 * filtered_games['OREB'] +
        0.3 * filtered_games['DREB'] +
        filtered_games['STL'] +
        0.7 * filtered_games['AST'] +
        0.7 * filtered_games['BLK'] -
        filtered_games['PF'] -
        filtered_games['TOV']
    )
    filtered_games.to_pickle(f'/Users/augustalexander/Navigator PER adjusted/df_{abbr}_{season_year}.pkl')

    return filtered_games.head().to_dict(orient='records')


if __name__ == "__main__":
    abbr = sys.argv[1]
    season_year = sys.argv[2]
    data = fetch_and_process_data(abbr, season_year)
    print(data)  # Optionally convert this print to a JSON serialization if running standalone
