#Import packages
import utils.runtime as rt
import utils.network as net

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

from sklearn.linear_model import PoissonRegressor

#Load the pulled dataset
def load_data(settings):
    
    #Get the full table name
    full_table = (f"[{settings["sql_database"]}].[{settings["sql_schema"]}]." 
                    + f"[{settings["sql_preprocessing_destination"]}]")

    load_query = f"SELECT * FROM {full_table}"

    engine = net.db_connect(settings["sql_dsn"], settings["sql_database"])
    df = net.load_data(settings, load_query, "query", engine)

    return df

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
    
    #Encode non-numeric columns
    ##########################################################################################

    #Normalise numeric features
    scaler = MinMaxScaler()
    X_train_norm = scaler.fit_transform(X_train)
    X_test_norm = scaler.fit_transform(X_test)

    return X_train, X_test, y_train, y_test

def main():
    #Load the runtime settings
    settings = rt.load_settings()

    #Load the data
    df = load_data(settings)

    X_train, X_test, y_train, y_test = data_split(
        df, target="los", 
        test_size=0.2,
        rs=0)

main()