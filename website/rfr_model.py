import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import StandardScaler
import joblib

df = pd.read_csv('data_prevgrade.csv')

features = df[['attendance', 'financial_situation', 'learning_environment', 'previous_grades']]
labels = df['grades']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, labels, test_size=0.2, random_state=19)

rfr = RandomForestRegressor(random_state=13)

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=rfr, param_grid=param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)

best_rfr = grid_search.best_estimator_


# Saving the trained model and scaler to a file
joblib.dump(best_rfr, 'random_forest_model.pkl')
joblib.dump(scaler, 'scaler.pkl')
