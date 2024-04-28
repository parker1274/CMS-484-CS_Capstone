"""
File for creating the models

Will take the following inputs:
- model_type (Classifier or regressor for now, others later)
- TeamA_abbreviation (Team for the outcome we want)
- TeamB_abbreviation (Other team in the matchup)
- season (Always the current season, then goes back based on the number of season)
- number_seasons (Number of seasons we want going back for the current season)
- number_past_games (The number of recent games we want to get the average stats from for the model)
"""

from model_creation.decision_tree_model import game_outcome_model
from model_creation.multi_stat_model import predicted_stats_model
from model_creation.efe_realtime_model import create_controllable_both_teams

from tqdm import tqdm
import time



def create_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons):

    print(model_type)
    print(TeamA_abbreviation)

    # Check which model is to be created
    if (model_type == "classifier"):
        print(f"Creating a classifier model for {TeamA_abbreviation}")
        game_outcome_model(TeamA_abbreviation, TeamB_abbreviation, season, number_seasons)
    
    elif (model_type == "regressor"):
        print(f"Creating a regressor model for {TeamA_abbreviation}")
        predicted_stats_model(TeamA_abbreviation, TeamB_abbreviation, season, number_seasons)

    elif (model_type == "controllable"):
        print(f"Creating a controllable models for {TeamA_abbreviation} & {TeamB_abbreviation}")
        create_controllable_both_teams(TeamA_abbreviation, TeamB_abbreviation)

    else:
        print("The model type entered was not found.")

create_model("classifier", "BOS", "NYK", "2023-24", 3)


def create_multiple_models(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons):
    # Function to simulate creating models
    print(f"Creating {model_type} model for {TeamA_abbreviation} vs {TeamB_abbreviation}")

    # Check which model is to be created
    if model_type == "classifier":
        print(f"Classifier model created for {TeamA_abbreviation} vs {TeamB_abbreviation}")
        # Simulate game outcome modeling
        game_outcome_model(TeamA_abbreviation, TeamB_abbreviation, season, number_seasons)
    
    elif model_type == "regressor":
        print(f"Regressor model created for {TeamA_abbreviation} vs {TeamB_abbreviation}")
        # Simulate predicted stats modeling
        predicted_stats_model(TeamA_abbreviation, TeamB_abbreviation, season, number_seasons)

    elif model_type == "controllable":
        print(f"Controllable model created for {TeamA_abbreviation} & {TeamB_abbreviation}")
        # Simulate creating controllable models for both teams
        create_controllable_both_teams(TeamA_abbreviation, TeamB_abbreviation)

    else:
        print("The model type entered was not found.")

# List of matchups as tuples
matchups = [
    ("ORL", "CLE"),  # Orlando Magic vs. Cleveland Cavaliers
    ("LAL", "DEN"),  # Los Angeles Lakers vs. Denver Nuggets
    ("BOS", "MIA"),  # Boston Celtics vs. Miami Heat
    ("PHI", "NYK"),  # Philadelphia 76ers vs. New York Knicks
    ("MIL", "IND"),  # Milwaukee Bucks vs. Indiana Pacers
    ("OKC", "NOP"),  # Oklahoma City Thunder vs. New Orleans Pelicans
    ("LAC", "DAL"),  # Los Angeles Clippers vs. Dallas Mavericks
    ("MIN", "PHX")   # Minnesota Timberwolves vs. Phoenix Suns
]


# Model types to create
model_types = ["classifier", "regressor", "controllable"]

# Season and number of seasons to consider for the modeling
season = "2023-24"
number_seasons = 3



# start_time = time.time()  # Start timing before the loop starts

# # Loop over each matchup and create models of each type
# for teamA, teamB in tqdm(matchups, desc="Matchups"):
#     for model_type in tqdm(model_types, desc="Model Types", leave=False):
#         create_model(model_type, teamA, teamB, season, number_seasons)

# end_time = time.time()  # End timing after the loop finishes
# total_time = end_time - start_time  # Calculate total duration
# print(f"Total execution time: {total_time:.2f} seconds")  # Print the total execution time