import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, GridSearchCV, RandomizedSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from sklearn.ensemble import RandomForestClassifier

import matplotlib.pyplot as plt
import time
from scipy.stats import randint
import shap




# Specify the path to your CSV file
file_path = '/Users/jkran/code/school/CMS-484-CS_Capstone/backend/BOS_2022-23_games.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)



# Convert 'WL' column to a binary 'Win' column, 1 for a win ('W') and 0 for a loss ('L')
df['Win'] = df['WL'].apply(lambda x: 1 if x == 'W' else 0)

# Make a new feature based on the interactions between the variables
df['PTS_PER_ATTEMPT'] = df['PTS'] / (df['FGA']) # + df['FTA']

print(df['PTS_PER_ATTEMPT'])


# Select features and target variable
features = df[['FG_PCT', 'FG3_PCT', 'FT_PCT', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PTS_PER_ATTEMPT']]
target = df['Win']



# Split the data
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Train the decision tree
start_time = time.time()
tree = DecisionTreeClassifier(max_depth=6, random_state=42)
tree.fit(X_train, y_train)

# Predict and evaluate
predictions = tree.predict(X_test)
end_time = time.time()

# Classification Report
print(classification_report(y_test, predictions))

# Calculate metrics
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions)
recall = recall_score(y_test, predictions)
f1 = f1_score(y_test, predictions)

print(f"Model Performance:\nAccuracy: {accuracy}\nPrecision: {precision}\nRecall: {recall}\nF1 Score: {f1}")
print(f"Training and Prediction Time: {end_time - start_time} seconds\n")

# Visualize the decision tree
plt.figure(figsize=(15, 8))
plot_tree(tree, filled=True, feature_names=features.columns, class_names=['Loss', 'Win'], rounded=True, fontsize=12)
# plt.show()
# plt.close('all')

# Save the figure
# Extract the season from the CSV filename for dynamic naming
season = 'BOS_2022-23'.split('_games.csv')[0]  # Adjust the string slicing based on your filename structure
output_filename = f"{season}_DT.png"
plt.savefig(output_filename)



def grid_hyperparamter(X_train, X_test, y_train, y_test):

    # Hyperparameter tuning with GridSearchCV
    param_grid = {
        'max_depth': [None, 5, 10, 15, 20, 25, 30],
        'min_samples_split': [2, 5, 10, 15, 20],
        'min_samples_leaf': [1, 2, 4, 6, 8],
    }

    grid_search = GridSearchCV(DecisionTreeClassifier(random_state=42), param_grid, cv=5)
    grid_search.fit(X_train, y_train)  # Use the unscaled X_train here
    best_tree = grid_search.best_estimator_

    # Implement changes as per the suggestions
    # For example, using the best model after hyperparameter tuning

    # Record start time
    start_time = time.time()

    # Train your new model and make predictions
    best_tree.fit(X_train, y_train)  # Use the unscaled X_train here
    new_predictions = best_tree.predict(X_test)  # Use the unscaled X_test here

    # Record end time
    end_time = time.time()

    # Calculate and print new model performance metrics
    new_accuracy = accuracy_score(y_test, new_predictions)
    new_precision = precision_score(y_test, new_predictions)
    new_recall = recall_score(y_test, new_predictions)
    new_f1 = f1_score(y_test, new_predictions)

    print(f"Grid Search Performance:\nAccuracy: {new_accuracy}\nPrecision: {new_precision}\nRecall: {new_recall}\nF1 Score: {new_f1}")
    print(f"Training and Prediction Time: {end_time - start_time} seconds\n")

    # Visualize the decision tree
    plt.figure(figsize=(15, 8))
    plot_tree(best_tree, filled=True, feature_names=features.columns, class_names=['Loss', 'Win'], rounded=True, fontsize=12)
    plt.show()

    return best_tree



def rand_hyperparamter():
    # Define the parameter space to sample from
    param_dist = {
        'max_depth': [3, None] + list(range(5, 21, 5)),  # None means no limit
        'min_samples_split': randint(2, 11),
        'min_samples_leaf': randint(1, 11),
    }

    # Initialize the model
    tree = DecisionTreeClassifier(random_state=42)

    # Initialize RandomizedSearchCV with a DecisionTreeClassifier and the distribution
    random_search = RandomizedSearchCV(tree, param_distributions=param_dist, n_iter=100, cv=5, verbose=1, random_state=42, n_jobs=-1)

    # Record start time of RandomizedSearchCV
    start_time = time.time()
    
    # Fit RandomizedSearchCV to the training data
    random_search.fit(X_train, y_train)
    
    # Use the best model
    best_tree = random_search.best_estimator_

    # Record end time of RandomizedSearchCV and calculate duration
    end_time = time.time()
    duration = end_time - start_time

    # Make predictions with the best model
    predictions = best_tree.predict(X_test)

    # Calculate and print model performance metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    print(f"RandomizedSearchCV Model Performance:")
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")
    print(f"Optimization and Prediction Time: {duration} seconds\n")

def random_forest():
    # Initialize the model with default parameters
    rf = RandomForestClassifier(random_state=42)

    # Record start time
    start_time = time.time()

    # Fit the model to the training data
    rf.fit(X_train, y_train)

    # Make predictions on the test set
    predictions = rf.predict(X_test)

    # Record end time and calculate duration
    end_time = time.time()
    duration = end_time - start_time

    # Calculate and print model performance metrics
    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions)
    recall = recall_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    print(f"Random Forest Model Performance (Default Parameters):")
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")
    print(f"Training and Prediction Time: {duration} seconds")

def generate_shap_plots(model, X_test, feature_names):
    """
    Generates and plots SHAP values for a given model and test dataset.
    
    This function now checks for DecisionTreeClassifier, RandomForestClassifier,
    and models optimized with GridSearchCV or RandomizedSearchCV.

    Parameters:
    - model: The trained machine learning model or a model wrapped by GridSearchCV/RandomizedSearchCV.
    - X_test: The test dataset features (as a pandas DataFrame).
    - feature_names: List of feature names (as a list of strings).
    """
    # If the model is wrapped by GridSearchCV or RandomizedSearchCV, use the best estimator
    if isinstance(model, (GridSearchCV, RandomizedSearchCV)):
        model = model.best_estimator_
    
    # Initialize the SHAP explainer based on the model type
    if isinstance(model, (RandomForestClassifier, DecisionTreeClassifier)):
        explainer = shap.TreeExplainer(model)
    else:
        # For other model types, use a generic Explainer as a fallback
        explainer = shap.Explainer(model, X_test)
    
    # Compute SHAP values for the test set
    shap_values = explainer.shap_values(X_test)

    # Handle binary classification for tree-based models
    if isinstance(model, (RandomForestClassifier, DecisionTreeClassifier)) and isinstance(shap_values, list):
        # For binary classification models, SHAP values is a list with an element for each class
        shap_values_pos_class = shap_values[1]  # Assuming interest in the positive class
    else:
        # For regression, single output models, or non-tree based models
        shap_values_pos_class = shap_values

    # Generating SHAP summary plot
    shap.summary_plot(shap_values_pos_class, X_test)


    
    # # Get the expected value (the model output baseline)
    # expected_value = explainer.expected_value
    
    # # Ensure handling is correct for both binary classification and other model types
    # # For binary classification TreeExplainer, shap_values is a list with separate arrays for each class
    # if isinstance(shap_values, list):
    #     # Assuming positive class interest for binary classification models
    #     shap_values_for_plot = shap_values[1]
    # else:
    #     # For regression or single output models
    #     shap_values_for_plot = shap_values

    # # Generate the decision plot for the positive class or the model's output
    # # Note: The decision plot visualizes the model’s decision for a single prediction, so we select one instance
    # instance_index = 0 # Example: Generate decision plot for the first instance in X_test
    # shap.decision_plot(expected_value, shap_values_for_plot[instance_index], X_test.iloc[instance_index])


# grid_hyperparamter()
# rand_hyperparamter()
# random_forest()
# generate_shap_plots(tree, X_test, feature_names=X_test.columns.tolist())




upcoming_game_features = pd.DataFrame([{
    'FG_PCT': 0.450,  # Field Goal Percentage
    'FG3_PCT': 0.350,  # Three-Point Field Goal Percentage
    'FT_PCT': 0.800,  # Free Throw Percentage
    'REB': 44,  # Rebounds
    'AST': 22,  # Assists
    'STL': 7,  # Steals
    'BLK': 5,  # Blocks
    'TOV': 14,  # Turnovers
    'PTS_PER_ATTEMPT': 1.2,  # Points per attempt (custom feature)
}])

# Making a prediction with the Decision Tree model
prediction = tree.predict(upcoming_game_features)

# Interpret the prediction
if prediction[0] == 1:
    print("The model predicts a win for the team.")
else:
    print("The model predicts a loss for the team.")



