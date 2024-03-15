import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Specify the path to your CSV file
file_path = '/Users/jkran/code/school/CMS-484-CS_Capstone/backend/BOS_2022-23_games.csv'

# Read the CSV file into a DataFrame
data = pd.read_csv(file_path)



# Display the first few rows of the dataframe
# print(data.head())

# # Get a concise summary of the dataframe
# print(data.info())

# # Generate descriptive statistics
# print(data.describe())


# Select only numerical columns
numerical_data = data.select_dtypes(include=['float64', 'int64'])

numerical_data = numerical_data.drop(columns=['GAME_ID'])


# Correlation Heatmap
plt.figure(figsize=(20, 15))
corr_matrix = numerical_data.corr()
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, linewidths=.5, cbar_kws={"shrink": .5})
plt.title('Correlation Matrix')
plt.show()

# Pair Plot for a Subset of Variables
# Given the large number of variables, you might want to focus on a few at a time
subset_data = numerical_data[['PTS', 'FGM', 'FGA', 'FG_PCT', 'REB', 'AST', 'STL', 'TOV', 'PLUS_MINUS']]
sns.pairplot(subset_data)
plt.suptitle('Pair Plot of Selected Variables', y=1.02)  # Adjusts the title position
plt.show()

# Histograms for Individual Variable Distributions
variables_for_histogram = ['PTS', 'REB', 'AST', 'STL', 'TOV', 'PLUS_MINUS']
fig, axes = plt.subplots(nrows=len(variables_for_histogram), ncols=1, figsize=(8, 4 * len(variables_for_histogram)))
for i, var in enumerate(variables_for_histogram):
    sns.histplot(data[var], kde=True, ax=axes[i])
    axes[i].set_title(f'Distribution of {var}')
    axes[i].set_xlabel('')
plt.tight_layout()
plt.show()