import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ['name', 'salary', 'player_id', 'birthDate', 'birthPlace', 'career_AST',
#        'career_FG%', 'career_FG3%', 'career_FT%', 'career_G', 'career_PER',
#        'career_PTS', 'shoots', 'weight', 'season_start', 'season_end', 'team',
#        'career_TRB', 'career_WS', 'career_eFG%', 'college', 'draft_pick',
#        'draft_round', 'draft_team', 'draft_year', 'height', 'highSchool',
#        'position'],

# Example: Read data from a CSV file
data = pd.read_csv('master_data.csv')

data['season_start'] = pd.to_numeric(data['season_start'], errors='coerce')

# Filter the data
filtered_data = data[data['season_start'] > 2010]

# Display the filtered data
# print(filtered_data)

# Scatter Plot
plt.scatter(data['height'], data['salary'])
plt.xlabel('Career Games Played')
plt.ylabel('Salary')
plt.title('Scatter Plot of Career Games Played vs. Salary')
plt.show()

# # Pair Plot
# numerical_features = ['career_G', 'career_PTS', 'career_WS', 'height', 'weight', 'career_FG%']
# sns.pairplot(data[numerical_features + ['salary']])
# plt.show()

# # Correlation Matrix
# correlation_matrix = data.corr()
# sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
# plt.title('Correlation Matrix')
# plt.show()


# import pandas as pd

# # Replace 'your_file.csv' with the path to your CSV file
# file_path = 'master_data.csv'

# # Read the CSV file into a DataFrame
# data = pd.read_csv(file_path)

# # Print the DataFrame
# print(data.columns)
