import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def data_manipulation(year):
    data = pd.read_csv('master_data.csv')

    data['season_start'] = pd.to_numeric(data['season_start'], errors='coerce')
    year_filtered_data = data[data['season_start'] >= year]

    print(year_filtered_data)

    # ==============outliers========================

    # Exclude non-numeric columns
    numerical_columns = ['career_AST', 'career_FG%', 'career_FG3%', 'career_FT%', 'career_G', 'career_PER', 'career_PTS', 'career_TRB', 'career_WS', 'career_eFG%']
    year_filtered_data[numerical_columns] = year_filtered_data[numerical_columns].apply(pd.to_numeric, errors='coerce')

    # Calculate quantiles and IQR after excluding non-numeric columns
    Q1 = year_filtered_data[numerical_columns].quantile(0.25)
    Q3 = year_filtered_data[numerical_columns].quantile(0.75)
    IQR = Q3 - Q1

    # Define a threshold for identifying outliers (e.g., 1.5 times the IQR)
    outlier_threshold = 2

    # Create a boolean mask for outliers
    outlier_mask = ((year_filtered_data[numerical_columns] < (Q1 - outlier_threshold * IQR)) | (year_filtered_data[numerical_columns] > (Q3 + outlier_threshold * IQR)))

    # Remove rows with outliers
    data_no_outliers = year_filtered_data[~outlier_mask.any(axis=1)]

    # Display the DataFrame without outliers
    print(data_no_outliers)
    return data_no_outliers

def graph(data):
    # Scatter Plot
    plt.scatter(data['career_FT%'], data['salary'])
    plt.xlabel('career_FG%')
    plt.ylabel('Salary')
    plt.title('Scatter Plot of Career Games Played vs. Salary')
    plt.show()

    # Pair Plot
    # numerical_features = ['career_G', 'career_PTS', 'career_WS', 'height', 'weight', 'career_FG%']
    # sns.pairplot(data[numerical_features + ['salary']])
    # plt.show()

    # # Correlation Matrix
    # correlation_matrix = data.corr()
    # sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    # plt.title('Correlation Matrix')
    # plt.show()

def main():
    year = int(input("Start year (1985-2018) "))
    data_no_outliers = data_manipulation(year)
    graph(data_no_outliers)

if __name__ == "__main__":
    main()
