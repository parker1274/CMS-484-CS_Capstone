from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import teams



import warnings
from urllib3.exceptions import InsecureRequestWarning



warnings.simplefilter('ignore', InsecureRequestWarning)



from nba_api.stats.static import players

# get_teams returns a list of 30 dictionaries, each an NBA team.
nba_teams = teams.get_teams()
print("Number of teams fetched: {}".format(len(nba_teams)))
nba_teams[:3]

# get_players returns a list of dictionaries, each representing a player.
spurs = [team for team in nba_teams if team["full_name"] == "San Antonio Spurs"][0]
spurs

print(spurs)