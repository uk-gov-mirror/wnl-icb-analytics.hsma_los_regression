#Import packages
import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.linear_model import PoissonRegressor

import utils.runtime as rt
import utils.network as net

#Load the pulled dataset
def load_data(settings):
    
    #Connect to DB
    engine = net.db_connect(settings["sql_dsn"], settings["sql_database"])

    #SUS Spell data
    df_base = net.load_data(
        settings, "script_sfw_preprocessing", "sql", engine)
    
    return df_base

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
    
    return X_train, X_test, y_train, y_test

#Make adjustments for missing/unknown data
def adjust_missing(df):

    print("    Initial:", df.shape)
    
    #patient_gender#############################################################
    ## Remove rows with a NULL gender
    df.dropna(subset=["patient_gender"], inplace=True)

    print("    Remove NULL gender:", df.shape)

    #admission_method###########################################################
    ## Remove rows with a NULL admission method
    df.dropna(subset=["admission_method"], inplace=True)
    
    ## Remove rows with an admission method for the following:
    ## -1         Unknown
    ## 82, 83, 2C Related to the birth of a baby
    ## 99         Not known or data error
    ## 31, 32     Maternity which should be filtered out already
    admissions_filter = ["-1", "82", "83", "2C", "99", "31", "32"]
    df = df[~df["admission_method"].isin(admissions_filter)]
    
    print("    Remove Unknown admission method:", df.shape)

    ############################################################################

    return df

def feature_engineering(df):
    #Create a fresh copy to work from
    df = df.copy()

    #patient_gender#############################################################
    print("    Map numeric gender values to labels and remove unknowns")
    ## Map numeric values to readable labels
    df["patient_gender"] = df["patient_gender"].astype(int)
    df["patient_gender"] = df["patient_gender"].map({1: "Male", 2: "Female"})

    ## Remove values that failed to map:
    ## 0 - Not known, removed as small count
    ## 9 - Not specified, removed as small count
    df.dropna(subset=["patient_gender"], inplace=True)

    #admission_method###########################################################
    print("    Categorise admission into Emergency and Non-Emergency")
    ## Categorise between Emergency and Non-Emergency
    df["flag_emergency"] = df["admission_method"].str.startswith("2").astype(int)
    ## Drop the original column if no longer of use
    df = df.drop(labels="admission_method", axis=1)

    return df

#Apply transformer to scale numeric features and one hot categorical ones
def apply_transformer(df, transformer=None):

    #Get a list of columns for the dataset
    numeric_cols = df.select_dtypes(include='number').columns
    categorical_cols = df.select_dtypes(include='object').columns

    #If handling training data, create and fit the transformer
    if transformer is None:
        transformer = ColumnTransformer(transformers=[
            ('num', MinMaxScaler(), numeric_cols),
            ('cat', 
             OneHotEncoder(handle_unknown='ignore', sparse_output=False), 
             categorical_cols)
        ])
        
        df_trans = transformer.fit_transform(df)

    #Otherwise reuse the previously fit transformer
    else:
        df_trans = transformer.transform(df)

    #Get resulting One Hot Encoding columns output
    cat_features = (
        transformer.named_transformers_['cat'].get_feature_names_out(
            categorical_cols)
    )
    #Get full list of output columns
    output_features = list(numeric_cols) + list(cat_features)

    return pd.DataFrame(df_trans, columns=output_features), transformer

def preprocess(X, y, mode="set", weights={}):
    #Account for missing/unknown data
    print("-> Adjust for missing data")
    X = adjust_missing(X)

    #Derive new features
    print("\n-> Engineer new features")
    X = feature_engineering(X)

    #Remove values from the target that were removed from X during preprocessing
    y = y.loc[X.index]

    #Applying transformer
    print("\n-> Apply transformer")
    if mode == "set":
        X, w = apply_transformer(X)
        weights["transformer"] = w
    else:
        X, _ = apply_transformer(X, transformer=weights["transformer"])

    print("\n Data Preview")
    print(X.head())

    return X, y, weights

def main():
    #Load the runtime settings
    settings = rt.load_settings()

    #Load the data
    df = load_data(settings)

    #Split the data by major hospital site
    sites = settings["sites"]
    
    for site in sites:

        df_site = df.copy()[df["site_code"] == site]

        #Split the data into train and test
        X_train, X_test, y_train, y_test = data_split(
            df_site, target="los", 
            test_size=0.2,
            rs=0)
        
        #Process the training data
        print("X_train pre-processing:")
        X_train, y_train, weights_train = preprocess(X_train, y_train)
        
        print("\nX_test pre-processing:")
        X_test, y_test, _ = preprocess(X_test, y_test, 
                                    mode="apply", weights=weights_train)

        #Output the datasets
        path_prefix = f"./{settings["site_data_dir"]}{site}/"
        X_train = pd.concat([X_train, X_test])
        y_train = pd.concat([y_train, y_test])

        X_train.to_csv(path_prefix + "x_train" + ".csv", index=False)
        X_test.to_csv(path_prefix + "x_test" + ".csv", index=False)
        y_train.to_csv(path_prefix + "y_train" + ".csv", index=False)
        y_test.to_csv(path_prefix + "y_test" + ".csv", index=False)

        #Fit model
        model = PoissonRegressor()
        model.fit(X_train, y_train.values.ravel())

        pickle.dump(model, open(path_prefix + "model.sav", "wb"))

main()