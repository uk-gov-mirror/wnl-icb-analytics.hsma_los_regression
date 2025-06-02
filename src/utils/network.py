#Functions for interacting with the database

#Import packages
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, text, insert

#Establish a connection to the database
def db_connect(dsn, database):
    
    #Create Connection String
    conn_str = (f"mssql+pyodbc:///"
                f"?odbc_connect=DSN={dsn};"
                f"DATABASE={database};"
                f"Trusted_Connection=yes;")
    
    #Create SQL Alchemy Engine object
    engine = create_engine(conn_str, use_setinputsizes=False)
    return engine

#Sub function of load_data to execute SQL
def load_data_from_query(engine, query):
    with engine.connect() as con:
        res = pd.read_sql_query(query, con)

    return res

#Function to load data
def load_data(settings, src, src_type="sql", engine=None):
    #Handle SQL data sources
    if src_type == "sql":
        #Load .sql file
        with open(settings[src]) as file:
            query_sql = text(file.read())
        
        #Execute query
        return load_data_from_query(engine, query_sql)
    
    #Execute a SFW string
    elif src_type == "query":
        return load_data_from_query(engine, text(src))
    
    #Handle csv data sources
    elif src_type == "csv":
        #Return file contents
        return pd.read_csv(settings[src])

#Function to upload data for a given dataset
def upload_data(df, engine, settings, 
                destination_table, create_script, batch_size=200):

    sql_database = settings["sql_database"]
    sql_schema = settings["sql_schema"]

    #Get the full table name
    full_table = (f"[{sql_database}].[{sql_schema}]." 
                  + f"[{destination_table}]")

    #Convert float columns to objects (Needed for dealing with NaNs)
    df = df.astype(object).where(pd.notnull(df), None)
    
    #Split the data into rows
    rows = df.to_dict(orient="records")

    #Re-create the destination table
    #   This is because the structure of the tables change frequently
    with engine.connect() as con:
        #Set the database
        con.execute(text(f"USE {sql_database};"))

        #Drop query
        try:
            query_drop = text(f"DROP TABLE {full_table}")
            con.execute(query_drop)
            con.commit()
        except:
            pass

        #Recreate the table
        with open(create_script) as file:
            create_query = text(file.read())
        con.execute(create_query)
    
        #Commit changes
        con.commit()

    #Bind the metadata to the destination table
    metadata = MetaData()
    sqlalc_table = Table(destination_table, metadata, 
                            schema=sql_schema, autoload_with=engine)

    #Insert the data
    with engine.begin() as con:  
        #Group the data into batches and upload
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i+batch_size]
            result = con.execute(
                insert(sqlalc_table),
                batch
            )

#Function to load the dataset with listed features filtered out
def load_features(settings, filters = []):
    #Connect to DB
    engine = db_connect(settings["sql_dsn"], settings["sql_database"])

    query_pull = (
        f"SELECT * FROM "
        f"[{settings["sql_database"]}]."
        f"[{settings["sql_destination_schema"]}]."
        f"[{settings["sql_destination_table"]}]"
    )
    df_features = load_data(
        settings, query_pull, src_type="query", engine=engine)

    #Remove parameter filters
    df_features = df_features.drop(columns=filters)

    return df_features