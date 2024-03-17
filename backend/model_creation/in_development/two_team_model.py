import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz


# Specify the path to your CSV file
file_path = '/Users/jkran/code/school/CMS-484-CS_Capstone/backend/BOS_PHI_2022-23_games.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

print(df)
# Ensure your target variable (win/loss) is encoded properly, 0 for loss and 1 for win
# If necessary, convert win/loss labels to 0/1
# Convert 'WL' column to a binary 'Win' column, 1 for a win ('W') and 0 for a loss ('L')
df['Win'] = df['WL'].apply(lambda x: 1 if x == 'W' else 0)

# Select features and target variable
features = df[['FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK', 'TOV',
               'OPP_FG_PCT', 'OPP_FG3_PCT', 'OPP_FT_PCT', 'OPP_REB', 'OPP_AST', 'OPP_STL', 'OPP_BLK', 'OPP_TOV']]  # Adjusted feature set
target = df['Win']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the decision tree
tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(X_train, y_train)

# Predict and evaluate
predictions = tree.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy}")


# Visualize the decision tree
plt.figure(figsize=(20, 10))
plot_tree(tree, filled=True, feature_names=features.columns, class_names=['Loss', 'Win'], rounded=True, fontsize=12)

# Extract the season from the CSV filename
season = 'BOS_PHI_2022-23_games.csv'.split('_games.csv')[0]
output_filename = f"{season}_DT.png"

# Save the figure with the new filename
plt.savefig(output_filename)

export_graphviz(tree, out_file='tree.dot', feature_names=['FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK', 'TOV', 
                                                          'OPP_FG_PCT', 'OPP_FG3_PCT', 'OPP_FT_PCT', 'OPP_REB', 'OPP_AST', 'OPP_STL', 'OPP_BLK', 'OPP_TOV'],
                     class_names=['Won', 'Lost'],  filled=True, rounded=True, special_characters=True,
                     proportion=True)


# Step 1: Prepare Your Input Data
# Example estimated statistics for an upcoming game
estimated_stats = {
        # 'PTS': 100,  # Fixed average points
        'FG_PCT': 0.46,  # Fixed field goal percentage
        'FG3_PCT': 0.35,  # Fixed three-point field goal percentage
        'FT_PCT': 0.80,  # Fixed free throw percentage
        'REB': 50,  # Fixed rebounds
        'AST': 30,  # Fixed assists
        'STL': 8,  # Fixed steals
        'BLK': 5,  # Fixed blocks
        'TOV': 15,  # Fixed turnovers
        'OPP_FG_PCT': 0.47,  # Fixed field goal percentage
        'OPP_FG3_PCT': 0.32,  # Fixed three-point field goal percentage
        'OPP_FT_PCT': 0.83,  # Fixed free throw percentage
        'OPP_REB': 48,  # Fixed rebounds
        'OPP_AST': 31,  # Fixed assists
        'OPP_STL': 7,  # Fixed steals
        'OPP_BLK': 6,  # Fixed blocks
        'OPP_TOV': 13  # Fixed turnovers
    }

# Step 2: Create a DataFrame for the Input
# Ensure the structure and order of features match those of the training data
input_data = pd.DataFrame([estimated_stats])

# If your model training involved feature scaling, apply the same scaling to your input data here
# scaler.transform(input_data)  # Assuming 'scaler' is your scaler object

# Step 3: Make the Prediction
prediction = tree.predict(input_data)

print(prediction)

# Step 4: Interpreting the Prediction
# Interpret the output based on how your model was trained
# For a binary classification model, 0 might represent a loss and 1 a win
if prediction[0] == 1:
    print("The model predicts a win for the team.")
else:
    print("The model predicts a loss for the team.")

# If your model supports it, you can also check the prediction probabilities
probabilities = tree.predict_proba(input_data)
print(f"Win Probability: {probabilities[0][1]:.2f}")
print(f"Loss Probability: {probabilities[0][0]:.2f}")

print()

