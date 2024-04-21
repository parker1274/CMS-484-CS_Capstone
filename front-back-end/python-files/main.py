# Import the json module to work with JSON data
import json
import sys

import pandas as pd
from joblib import dump, load



sys.path.append('/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/data_collection')
import feature_avgs



# Convert arguments to integers
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

model = load('/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/model_creation/classifier_models/BOS_NYK_2023-24_past_5_season_DT_model.joblib')


pickle_file_path = f"/Users/jkran/code/school/CMS-484-CS_Capstone/python-code/pickle_dataframes/df_{TeamA_abbreviation}_{TeamB_abbreviation}_{season}_past_{number_seasons}_season.pkl"
df = pd.read_pickle(pickle_file_path)

df.drop(['TeamA_WL'], axis=1, inplace=True)

# print(df)

feature_avg_df = feature_avgs.feature_avgs(df, number_past_games)

input_data = feature_avg_df

# Assuming input_data is a pandas Series
input_data_df = input_data.to_frame().T  # Transposes the Series to a DataFrame

# # Drop the columns that aren't features the model was trained on
input_data_df.drop(['pointsAgainst_diff', 'pointsAgainst_ratio', 'points_diff', 'points_ratio'], axis=1, inplace=True)


# Make predictions and retrieve probabilities
prediction = model.predict(input_data_df)
probabilities = model.predict_proba(input_data_df)

# # Output the model's prediction
# if prediction[0] == 1:
#     print(f"The model predicts a win for the team with a probability of {probabilities[0][1]:.2%}.")
# else:
#     print(f"The model predicts a loss for the team with a probability of {probabilities[0][0]:.2%}.")

# # Display both probabilities for clarity
# print(f"Win Probability: {probabilities[0][1]:.8%}")
# print(f"Loss Probability: {probabilities[0][0]:.8%}")



# Construct the dictionary with the relevant information
result_data = {
    "prediction_outcome": "Win" if prediction[0] == 1 else "Loss",
    "prediction_probability": f"{probabilities[0][1]:.2%}" if prediction[0] == 1 else f"{probabilities[0][0]:.2%}",
    "probabilities": {
        "win_probability": f"{probabilities[0][1]:.8%}",
        "loss_probability": f"{probabilities[0][0]:.8%}"
    }
}



# Use json.dumps() to convert the dictionary to a JSON string
# and print it so that Node.js can capture the output
print(json.dumps(result_data))
