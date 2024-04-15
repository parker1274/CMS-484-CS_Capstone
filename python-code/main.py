"""
Main file for calling run_models.py & create_models.py
"""
from create_models import create_model
from run_models import run_model
from aws_lambda_powertools import Logger
import json

LOGGER = Logger(level="DEBUG")

class InvalidRequestBodyError(Exception):
    pass

class IncorrectActionRequestError(Exception):
    pass

def lambda_handler(event, _):
    """
    Expected event:
    {
        "action": 1,
        "model_type": "classifier",
        "TeamA_abbreviation": "BOS",
        "TeamB_abbreviation": "NYK",
        "season": "2023-24",
        "number_seasons": 3,
        "number_past_games": 15
    }

    To run use:
    curl https://qr7cldaha9.execute-api.us-east-1.amazonaws.com \
    -H "Content-Type: application/json" \
    -d '{"action": "1", "model_type": "classifier", "TeamA_abbreviation": "BOS", "TeamB_abbreviation": "NYK", "season": "2023-24", "number_seasons": "3", "number_past_games": "15"}'
    """
    # event = json.loads(event)
    # try:
    body = json.loads(event["body"])
    action = int(body["action"])
    model_type = body["model_type"]
    TeamA_abbreviation = body["TeamA_abbreviation"]
    TeamB_abbreviation = body["TeamB_abbreviation"]
    season = body["season"]
    number_seasons = int(body["number_seasons"])
    number_past_games = int(body["number_past_games"])
    # except Exception as e:
        # raise InvalidRequestBodyError(f"You need to pass parameters. Error: {e}")

    LOGGER.info("Received event: " + json.dumps(body))

    if (action == 0):
        LOGGER.debug("Creating model")
        output = create_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons)
    elif (action == 1):
        LOGGER.debug("Running model")
        output = run_model(model_type, TeamA_abbreviation, TeamB_abbreviation, season, number_seasons, number_past_games)
    else:
        raise IncorrectActionRequestError("Incorrect action request")

    # Return the output as a JSON object by using json.dumps()
    # And a status code of 200 to indicate success
    return {
        "statusCode": 200,
        "body": json.dumps(output)
    }

if __name__ == "__main__":
    # Test the lambda_handler function
    lambda_handler('{"body": {"action": "1","model_type": "classifier","TeamA_abbreviation": "BOS","TeamB_abbreviation": "NYK","season": "2023-24","number_seasons": "3","number_past_games": "15"}}', None)

