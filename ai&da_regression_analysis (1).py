# -*- coding: utf-8 -*-
"""AI&DA Regression analysis

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/190VwUEPjuBmAhZqjjj126pv0qRfexZ14

PREDICTION ON HOUSE PRICES USING THE TRAIN AND TEST DATASET
"""

#Import libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import seaborn as sns
from math import sqrt

#Read and name train dataset 
train_data_link = "http://drive.google.com/uc?id=1TKrP4mE6rsq3effIecEhHV4BuYT-zbsk"
TrainDF = pd.read_csv(train_data_link)

#Read and name test dataset
test_data_link = "http://drive.google.com/uc?id=1f-VKXrqc_Hj8QY1TC5uU8AFNuSc7_Dt6"
TestDF = pd.read_csv(test_data_link)

TrainDF.describe()

TestDF.describe()

TrainDF.head()

TestDF.head()

# Separate the target variable from the features
y_train = TrainDF["price"]                          
X_train = TrainDF.drop(columns=["price"])           

y_test = TestDF["price"]
X_test = TestDF.drop(columns=["price"])

y_train.info()
X_train.info()

#Find Correlation coefficients
corr_coef = []
for col in X_train.columns:
    coef = np.corrcoef(X_train[col], y_train)[0, 1]
    corr_coef.append((col, coef))

    # Sort correlation coefficient in descending order
corr_coef.sort(key=lambda x: abs(x[1]), reverse=True)

# Print the strongest correlation
print(f"The strongest correlation is between {corr_coef[0][0]} and dependent variable, with coefficient of {corr_coef[0][1]:.2f}.")

# Sort correlation coefficient in descending order
corr_coef.sort(key=lambda x: abs(x[1]), reverse=True)
corr_coef

# Plot bar chart of correlation coefficients
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar([x[0] for x in corr_coef], [x[1] for x in corr_coef], label='Correlation Coefficient')
plt.xticks(rotation=90)
plt.title('Correlation Coefficients')
plt.xlabel('Features')
plt.ylabel('Correlation Coefficients')
plt.legend()
plt.show()

#model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict the target variable for the testing data
y_pred = model.predict(X_train)
print('Predicted target variable:', y_pred)

print(model.score(X_train, y_train))
print(model.score(X_test, y_test))

# Calculate and print the metrics
mse = mean_squared_error(y_test, y_pred [:len(y_test)])
mae = mean_absolute_error(y_test, y_pred [:len(y_test)])
r2 = r2_score(y_test, y_pred [:len(y_test)])

print("Mean Squared Error:", mse)
print("Mean Absolute Error:", mae)
print("R2 Score:", r2)

from sklearn.model_selection import GridSearchCV

# Define the hyperparameters to tune
params = {
    'fit_intercept': [True, False],
    'copy_X': [True, False],
    'n_jobs': [-1, 1, 2, 4],
    'positive': [True, False]
}

# Create a linear regression model
lr = LinearRegression()

# Create a grid search object
grid_search = GridSearchCV(lr, param_grid=params, cv=5, verbose=1)

# Fit the grid search to the data
grid_search.fit(X_train, y_train)

# Print the best hyperparameters
print("Best Hyperparameters:", grid_search.best_params_)

# Create a new Linear Regression model with the best hyperparameters
new_model = LinearRegression(copy_X=True, fit_intercept=True, n_jobs=-1, positive=True)

# Train the model on the entire training dataset
new_model.fit(X_train, y_train)

import seaborn as sns
import matplotlib.pyplot as plt

# calculate feature importance
results = permutation_importance(new_model, X_train, y_train, scoring='neg_mean_squared_error', n_repeats=10, random_state=0)

# calculate normalized importances
importances = np.abs(results.importances_mean) / np.max(np.abs(results.importances_mean))

# sort features by normalized importance scores
sorted_features = sorted(zip(importances, X_train.columns), reverse=True)

# create a dataframe from the sorted feature importances
SFI = pd.DataFrame(sorted_features, columns=['Normalized Importance', 'Feature Name'])

# plot the feature importance chart
plt.figure(figsize=(10, 6))
sns.barplot(x='Normalized Importance', y='Feature Name', data=SFI)
plt.title('Feature Importances')
plt.show()

# Fit the new model to the training data
new_model.fit(X_train, y_train)

# Make predictions on the test data
y_pred = new_model.predict(X_test)

# Calculate mean squared error, mean absolute error, and R2 score
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print the evaluation metrics
print("Mean Squared Error:", mse)
print("Mean Absolute Error:", mae)
print("R2 Score:", r2)

print(new_model.score(X_train, y_train))   
print(new_model.score(X_test, y_test))

print("Intercept: \n",new_model.intercept_)
print("Coefficients: \n",new_model.coef_)

# Predict on the test set
y_pred = new_model.predict(X_test)

# Create a DataFrame with the predicted values
submission_df = pd.DataFrame({'Predicted': y_pred})

# Save the predictions to a CSV file
submission_df.to_csv('submission.csv', index=False)

for i in range(10):
    print(f"Actual value: {y_test[i]}, Predicted value: {y_pred[i]}")

import os
print(os.getcwd())

!ls /content

from google.colab import files
files.download('submission.csv')

def make_plot(y_test, y_pred):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(y_test, y_pred, color='blue')
    ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'k--', lw=4)
    ax.set_xlabel('Actual')
    ax.set_ylabel('Predicted')
    plt.show()

make_plot(y_test, y_pred)