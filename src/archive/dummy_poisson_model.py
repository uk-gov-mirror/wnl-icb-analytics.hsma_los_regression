#Import packages
import numpy as np
import pandas as pd
import seaborn as sns

from matplotlib import pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import PoissonRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

#Function to generate dummy Poisson data
def generate_data(beta1=0.05, low=1, high=100, size=1000, plot=True):

    X = np.random.uniform(low=low, high=high, size=size)
    X = np.floor(X)
    lam = np.exp(beta1 * X)
    y = np.random.poisson(lam, size = len(lam))
    if plot:
        plt.scatter(X,y)
        plt.show()

    return X, y

#Function to split the data into train and test splits
def preprocessing(X, y, test_size=0.2, rs=0):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        random_state=rs,
        test_size=test_size)
    
    #Convert X to a 2D array
    X_train = X_train.reshape(-1, 1)
    X_test = X_test.reshape(-1, 1)

    #Scale the X data
    scaler = StandardScaler()
    scaler.fit(X_train)

    X_train_scaled = scaler.transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test

#Plot a scatter plot comparing y to y_pred
def plot_scatter_comparison(y, y_pred):
    plt.figure(figsize=(6, 6))
    sns.scatterplot(x=y, y=y_pred)
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title("Actual vs Predicted")
    plt.plot([min(y), max(y)], [min(y), max(y)], color='red', linestyle='--')
    plt.grid(True)
    plt.show()

#Plot a residual plot of y against y_pred
def plot_residual(y, y_pred):
    residuals = y - y_pred
    plt.figure(figsize=(6, 4))
    sns.histplot(residuals, kde=True)
    plt.title("Residuals Distribution")
    plt.xlabel("Residual")
    plt.show()

def run_model(model, X, y):
    #Make predictions on y
    y_pred = model.predict(X)

    #Round y_pred to integer predictions
    y = y.astype(int)
    y_pred = np.round(y_pred).astype(int)

    #Assess the model predictions
    mse = mean_squared_error(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    print(f"MSE: {mse:.2f}, MAE: {mae:.2f}, R2: {r2:.2f}")

    print("Accuracy:", accuracy_score(y, y_pred))
    print("Precision:", precision_score(y, y_pred, average='macro'))
    print("Recall:", recall_score(y, y_pred, average='macro'))
    print("F1 Score:", f1_score(y, y_pred, average='macro'))

    plot_scatter_comparison(y, y_pred)
    plot_residual(y, y_pred)

def main():
    #Generate the data
    X, y = generate_data(plot=False)

    #Generate the split data
    X_train, X_test, y_train, y_test = preprocessing(X, y)

    #Build the model
    model = PoissonRegressor()
    model.fit(X_train, y_train)

    #Run the model
    run_model(model, X_test, y_test)


main()

