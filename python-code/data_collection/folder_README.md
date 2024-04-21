# Data Collection Folder

## Description

The data collection folder is used to gather and export all player, team, game, and season data that will be used for general consumption or model creation

## Structure

- **season_gen_data.py**: 
Contians functions for general data gathering like:
- Fetching game ids for a specific team during a season
- Fetching basic game data for a specific team during a season
- Fetching basic game data for all team during a season

- **game_stats.py**:
Contains functions for complete data gathering:
- Fetching complete game data for a specific team based on game id
- Exporting complete game data in a json file

- **season_stats**:
Contains one fucntion for exporting complete game data for an entire season
- Utilizes season_gen_data for game ids and game_stats for complete game data
- Exports complete season data in a dataframe

- **live_data**:
Currently not utilized (3/16/24) but provides the most up to date game data