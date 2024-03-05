from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder
import pandas as pd

def fetch_and_export_team_data(team_abbreviation, season):
    # Get dictionary of NBA teams
    nba_teams = teams.get_teams()
    
    # Find team by abbreviation
    team = [team for team in nba_teams if team['abbreviation'] == team_abbreviation.upper()]
    if not team:
        print(f"Team not found for abbreviation: {team_abbreviation}")
        return
    team_id = team[0]['id']

    # Query for games where the specified team was playing in the given season
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, season_nullable=season, season_type_nullable='Regular Season')
    games = gamefinder.get_data_frames()[0]  # The first DataFrame of those returned is what we want

    # Optionally, filter the DataFrame further if needed (e.g., home games, wins, etc.)

    return games

    # Export to CSV
    csv_filename = f'{team_abbreviation}_{season}_games.csv'
    games.to_csv(csv_filename, index=False)
    print(f"Data exported to {csv_filename}")

def export_all_team_data(season):
    # Get dictionary of NBA teams
    nba_teams = teams.get_teams()
    
    # Initialize an empty DataFrame to store all teams' data
    all_teams_data = pd.DataFrame()
    
    for team in nba_teams:
        team_id = team['id']
        
        # Fetch the team's game data
        gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id, season_nullable=season, season_type_nullable='Regular Season')
        team_games = gamefinder.get_data_frames()[0]  # The first DataFrame returned contains the games
        
        # Append the team's data to the all_teams_data DataFrame
        all_teams_data = pd.concat([all_teams_data, team_games], ignore_index=True)

    # Export to CSV
    csv_filename = f'all_teams_{season}_games.csv'
    all_teams_data.to_csv(csv_filename, index=False)
    print(f"All teams' data exported to {csv_filename}")


def team_match_up_stats(team_abbreviation1, team_abbreviation2, season):
    
    # Run fetch_and_export_team_data for both teams
    team1_data = fetch_and_export_team_data(team_abbreviation1, season)
    team2_data = fetch_and_export_team_data(team_abbreviation2, season)

    






# Example usage
team_match_up_stats('BOS', 'NYK')

    
       






