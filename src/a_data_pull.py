#Import packages
import pandas as pd

import utils.runtime as rt
import utils.network as net

#Load the main dataset from SUS
def load_data(settings):
    
    #Connect to DB
    engine = net.db_connect(settings["sql_dsn"], settings["sql_database"])

    #SUS Spell data
    df_spl = net.load_data(settings, "data_pull_script", "sql", engine)
    
    return df_spl

def main():
    #Load the runtime settings
    settings = rt.load_settings()

    #Load the data
    df_spl = load_data(settings)

    print(df_spl.head())

    #Upload the data to the destination table
    engine = net.db_connect(settings["sql_dsn"], settings["sql_database"])
    net.upload_data(df_spl, engine, settings, batch_size=1600)

main()