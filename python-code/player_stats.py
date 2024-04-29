import os
import pandas as pd
from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
pd.set_option('display.max_columns', None)

def fetch_and_process_data():
    player_name = input("Enter player's name: ")
    season_year = input("Enter season year: ")
    start = int(input("Enter start index: "))
    limit = int(input("Enter limit: "))

    # Find player by name
    nba_players = players.get_players()
    user_player = [player for player in nba_players if player['full_name'].lower() == player_name.lower()]
    
    if not user_player:
        print(f"No player found with the name {player_name}")
        return None

    player_id = user_player[0]['id']
    filename = f'./df_{player_name}_{season_year}.pkl'
    
    # Check if the file already exists
    if os.path.exists(filename):
        df = pd.read_pickle(filename)
        data_slice = df.iloc[start:start+limit]
        return data_slice.to_dict(orient='records')

    # Fetch game logs for the player
    gamelog = playergamelog.PlayerGameLog(player_id=player_id, season=season_year)
    games = gamelog.get_data_frames()[0]

    # Calculate metrics such as Player Efficiency Rating
    games['Player_Efficiency_Rating'] = (
        (games['PTS'] + games['REB'] + games['AST'] + games['STL'] + games['BLK']) -
        (games['FGA'] - games['FGM']) -
        (games['FTA'] - games['FTM']) -
        games['TOV']
    )

    games.to_pickle(filename)
    return games.iloc[start:start+limit].to_dict(orient='records')

# If this script is executed as the main program, run the function
if __name__ == '__main__':
    result = fetch_and_process_data()
    if result:
        print(result)
