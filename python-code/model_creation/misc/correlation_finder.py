import pandas as pd
import numpy as np

# Specify the path to your CSV file
file_path = '/Users/jkran/code/school/CMS-484-CS_Capstone/backend/BOS_2022-23_games.csv'

# Read the CSV file into a DataFrame
data = pd.read_csv(file_path)

# Select only numerical columns
numerical_data = data.select_dtypes(include=['float64', 'int64'])

numerical_data = numerical_data.drop(columns=['GAME_ID'])

# Calculate the correlation matrix
corr_matrix = numerical_data.corr()

# Define a threshold for strong correlations
threshold = 0.7

# Find strong correlations in the correlation matrix
strong_corr = corr_matrix[abs(corr_matrix) > threshold]

# Exclude self-correlations by setting diagonal values to NaN
np.fill_diagonal(strong_corr.values, np.nan)

# Convert the matrix to a long format for easier analysis
corr_pairs = strong_corr.stack().reset_index()
corr_pairs.columns = ['Variable 1', 'Variable 2', 'Correlation']

# Sort the variable names in each pair to ensure uniqueness
corr_pairs['Sorted Variables'] = corr_pairs.apply(lambda x: '-'.join(sorted([x['Variable 1'], x['Variable 2']])), axis=1)

# Drop duplicate pairs
corr_pairs = corr_pairs.drop_duplicates(subset=['Sorted Variables'])

# Drop the 'Sorted Variables' column as it's no longer needed
corr_pairs = corr_pairs.drop('Sorted Variables', axis=1)

# Filter out pairs with strong correlations
strong_pairs = corr_pairs.dropna(subset=['Correlation'])

# Display the strong correlation pairs
print("Strong Correlation Pairs (Above Threshold of {:.2f}):".format(threshold))
print(strong_pairs)
