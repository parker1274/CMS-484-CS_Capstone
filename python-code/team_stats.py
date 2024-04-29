import sys
import json
import os
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
pd.set_option('display.max_columns', None)

def fetch_and_process_data(abbr, season_year, start=0, limit=5):
    try:
        filename = f'/Users/augustalexander/VsCode/CMS-484-CS_Capstone/python-code/team_stat_archive/df_{abbr}_{season_year}.pkl'
        start = int(start)
        limit = int(limit)
        # Check if the file already exists
        if os.path.exists(filename):
            df = pd.read_pickle(filename)
            data_slice = df.iloc[int(start):int(start)+int(limit)]
            return data_slice.to_dict(orient='records')
        
        nba_teams = teams.get_teams()
        user_team = [team for team in nba_teams if team['abbreviation'] == abbr][0]
        team_id = user_team['id']

        gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, season_nullable=season_year, season_type_nullable= 'Regular Season')
        games = gamefinder.get_data_frames()[0]

        season_input = '2' + season_year
        filtered_games = games[games['SEASON_ID'] == season_input].copy()
        print(filtered_games.isnull().sum())  # Print the count of NaN values by column before fillna
        filtered_games.fillna(0, inplace=True)
        print(filtered_games.isnull().sum())  # Verify no NaN values exist after fillna

        # Calculate metrics such as Team Efficiency
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

        filtered_games['FT_PCT'].fillna(0, inplace=True)
        filtered_games.to_pickle(filename)
        return filtered_games.head(limit).to_dict(orient='records')
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print(json.dumps({"error": "Usage: python team_stats.py <team_abbr> <year> <start> <limit>"}))
        sys.exit(1)
    abbr = sys.argv[1]
    season_year = sys.argv[2]
    start = int(sys.argv[3])  # Convert start to integer
    limit = int(sys.argv[4])  # Convert limit to integer

    result = fetch_and_process_data(abbr, season_year, start, limit)
    print(json.dumps(result))  # ensure output is JSON formatted
