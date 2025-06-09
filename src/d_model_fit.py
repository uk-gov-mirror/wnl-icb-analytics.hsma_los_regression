#Import packages
import utils.runtime as rt
import utils.network as net

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

from sklearn.linear_model import PoissonRegressor

import utils.evaluation as ev

#Load the pulled dataset
def load_data(settings):
    
    #Get the full table name
    full_table = (f"[{settings["sql_database"]}].[{settings["sql_schema"]}]." 
                    + f"[{settings["sql_preprocessing_destination"]}]")

    load_query = f"SELECT * FROM {full_table}"

    engine = net.db_connect(settings["sql_dsn"], settings["sql_database"])
    df = net.load_data(settings, load_query, "query", engine)

    return df

#Perform the train test split for the data
def data_split(df, target, test_size=0.2, rs=42):
    features = list(df.columns)
    features.remove(target)

    X = df[features]
    y = df[target]

    #Apply test train split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        random_state=rs,  
        test_size=test_size, 
        shuffle=True)
    
    numeric_cols = X_train.select_dtypes(include='number').columns
    categorical_cols = X_train.select_dtypes(include='object').columns
    
    # Build transformer
    # MinMaxScaler for numeric columns
    # One Hot Encoding for categorical columns
    preprocessor = ColumnTransformer(transformers=[
        ('num', MinMaxScaler(), numeric_cols),
        ('cat', 
         OneHotEncoder(handle_unknown='ignore', sparse_output=False), 
         categorical_cols)
    ])

    #Apply transformations
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    #Get resulting One Hot Encoding columns output
    cat_features = (
        preprocessor.named_transformers_['cat'].get_feature_names_out(
            categorical_cols)
    )
    #Get full list of output columns
    output_features = list(numeric_cols) + list(cat_features)

    #Convert back into dataframes
    X_train_processed = pd.DataFrame(X_train_processed, columns=output_features)
    X_test_processed = pd.DataFrame(X_test_processed, columns=output_features)

    return X_train_processed, X_test_processed, y_train, y_test

def generate_data(beta1=0.05, low=1, high=100, size=1000, plot=True):

    X = np.random.uniform(low=low, high=high, size=size)
    X = np.floor(X)
    lam = np.exp(beta1 * X)
    y = np.random.poisson(lam, size = len(lam))

    df = pd.DataFrame({
    'feature': X,
    'los': y
    })

    return df

def main():
    #Load the runtime settings
    settings = rt.load_settings()

    #Load the data
    df = load_data(settings)

    #Load dummy data to test the model
    #df = generate_data()

    #Split the data into train test splits
    X_train, X_test, y_train, y_test = data_split(
        df, target="los", 
        test_size=0.2,
        rs=0)
    
    #Fit the model
    model = PoissonRegressor()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print(X_train.columns)

    #Evaluate results
    ev.plot_prediction_against_actual(y_test, y_pred)


main()