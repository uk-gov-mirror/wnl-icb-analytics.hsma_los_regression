#Import packages
import utils.runtime as rt
import utils.network as net

#Load the pulled dataset
def load_data(settings):
    
    #Connect to DB
    engine = net.db_connect(settings["sql_dsn"], settings["sql_database"])

    #SUS Spell data
    df_spl = net.load_data(
        settings, "script_preprocessing_source", "sql", engine)
    
    return df_spl

#Make adjustments for missing/unknown data
def adjust_missing(df):

    print(df.shape)
    
    #patient_gender#############################################################
    ## Remove rows with a NULL gender
    df.dropna(subset=["patient_gender"], inplace=True)

    print(df.shape)

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
    
    print(df.shape)

    ############################################################################

    return df

def feature_engineering(df):
    #patient_gender#############################################################
    ## Map numeric values to readable labels
    df["patient_gender"] = df["patient_gender"].astype(int)
    df["patient_gender"] = df["patient_gender"].map({1: "Male", 2: "Female"})

    ## Remove values that failed to map:
    ## 0 - Not known, removed as small count
    ## 9 - Not specified, removed as small count
    df.dropna(subset=["patient_gender"], inplace=True)

    #admission_method###########################################################
    ## Categorise between Emergency and Non-Emergency
    df["flag_emergency"] = df["admission_method"].str.startswith("2")
    ## Drop the original column if no longer of use
    df = df.drop(labels="admission_method", axis=1) 

    print(df.head())

    return df

def main():
    #Load the runtime settings
    settings = rt.load_settings()

    #Load the data
    df = load_data(settings)

    #Account for missing/unknown data
    df = adjust_missing(df)

    #Derive new features
    df = feature_engineering(df)

    #Upload the processed data
    engine = net.db_connect(settings["sql_dsn"], settings["sql_database"])
    net.upload_data(df, engine, settings, 
                    settings["sql_preprocessing_destination"], 
                    settings["script_preprocessing_create"], 
                    batch_size=1600)

main()