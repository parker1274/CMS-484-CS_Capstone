"""
Main file for calling run_models.py & create_models.py
"""


from create_models import create_model
from run_models import run_model



# action, model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games
action = 1 # 0 for create & 1 for run
model_type = "classifier"
TeamA_abbreviation = "BOS"
TeamB_abbreviation = "NYK"
season = "2023-24"
number_seasons = 3
# Number of past games used to create the average stats
number_past_games = 15




print("TEST")

if (action == 0):
    print("Creating model")
    create_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons)

elif (action == 1):
    print("Running model")
    run_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games)

else:
    print("Incorrect action request")







