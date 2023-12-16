import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import numpy as np

numerical_column = [
    "career_G",
    "career_PER",
    "career_PTS",
    "career_AST",
    "career_TRB",
    "career_WS",
    "career_eFG%",
    "draft_year",
    "combined_draft",
    "career_FG%",
    "career_FG3%",
    "career_FT%",
]

def data_manipulation(year):
    data = pd.read_csv("master_data.csv")
    # print(data)
    year_filtered_data = data[data["season_start"] >= year]
    year_filtered_data = year_filtered_data[year_filtered_data["career_G"] >= 50]

    numerical_columns = [
        "career_AST",
        "career_FG%",
        "career_FG3%",
        "career_FT%",
        "career_G",
        "career_PER",
        "career_PTS",
        "career_TRB",
        "career_WS",
        "career_eFG%",
        "salary",
        "weight",
        "height",
        "draft_year",
        "season_start",
        "season_end",
    ]

    year_filtered_data[numerical_columns] = year_filtered_data[numerical_columns].apply(
        pd.to_numeric, errors="coerce"
    )

    Q1 = year_filtered_data[numerical_columns].quantile(0.25)
    Q3 = year_filtered_data[numerical_columns].quantile(0.75)
    IQR = Q3 - Q1
    outlier_threshold = 1.4
    outlier_mask = (
        year_filtered_data[numerical_columns] < (Q1 - outlier_threshold * IQR)
    ) | (year_filtered_data[numerical_columns] > (Q3 + outlier_threshold * IQR))
    data_no_outliers = year_filtered_data[~outlier_mask.any(axis=1)]
    # print(data_no_outliers)
    return data_no_outliers

def graph(data):
    numerical_data = data[numerical_column]
    correlation_matrix = numerical_data.corr()

    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix')
    plt.show()


def AI(data, k=10):
    # dropna() removes all Nan
    data=data.fillna(0)
    # print(data)

    # Split data
    X_training, X_testing, y_training, y_testing = train_test_split(
        data[numerical_column], data['salary'], test_size=0.4, random_state=42
    )

    scaler = StandardScaler()
    X_training_scaled = scaler.fit_transform(X_training)
    X_testing_scaled = scaler.transform(X_testing)

    # Random Forest model
    rf_model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=47)
    rf_model.fit(X_training_scaled, y_training)

    # Predictions
    y_pred_rf = rf_model.predict(X_testing_scaled)

    # Evaluation of model
    r2_rf = r2_score(y_testing, y_pred_rf)
    print(f"R-squared (Random Forest): {r2_rf}")
    r2_scores = cross_val_score(rf_model, X_training_scaled, y_training, cv=k, scoring='r2')
    print(f"Cross-validated R^2 (k={k}):", r2_scores.mean())

    return rf_model, scaler

def predict_salary(model, scaler, input_values):
    input_values_scaled = scaler.transform([list(input_values.values())])

    predicted_salary = model.predict(input_values_scaled)

    return predicted_salary[0]

def wow_factor(wow,input):
    print("wow")

def main():
    # year = int(input("Start year (1985-2018) "))
    year=1985
    clean_data = data_manipulation(year)
    model, scaler = AI(clean_data)
    # 1=bench player 2= role player 3= all star 4= goat debate
    wow=1
    input_values = {
        "career_G": 904,
        "career_PER": 22,
        "career_PTS": 24.5,
        "career_AST": 5.9,
        "career_TRB": 5,
        "career_WS": 48,
        "career_eFG%": 59.1,
        "draft_year": 2009,
        "combined_draft": 111,
        "career_FG%":45.3,
        "career_FG3%":30,
        "career_FT%":81,
    }
    wow_factor(wow,input_values)

    prediction = predict_salary(model, scaler, input_values)

    print(f"Predicted Salary: {prediction}")

if __name__ == "__main__":
    main()
