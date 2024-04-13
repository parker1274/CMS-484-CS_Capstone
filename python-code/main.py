"""
Main file for calling run_models.py & create_models.py
"""
import json
import sys

from create_models import create_model
from run_models import run_model



# # action, model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games
# action = 1 # 0 for create & 1 for run
# model_type = "classifier"
# TeamA_abbreviation = "BOS"
# TeamB_abbreviation = "NYK"
# season = "2023-24"
# number_seasons = 3
# # Number of past games used to create the average stats
# number_past_games = 15

action = 1
model_type = sys.argv[1]
TeamA_abbreviation = sys.argv[2]
TeamB_abbreviation = sys.argv[3]
season = sys.argv[4]
try:
    number_seasons = int(sys.argv[5])
except (ValueError, IndexError) as e:
    print(f"Error converting input to integer: {e}")
    sys.exit(1)
number_past_games = int(sys.argv[6])

# print(TeamA_abbreviation)



# print("TEST")

if (action == 0):
    print("Creating model")
    create_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons)

elif (action == 1):
    # print("Running model")
    run_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games)

else:
    print("Incorrect action request")







