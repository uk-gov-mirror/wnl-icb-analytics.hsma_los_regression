#Functions for interacting with the database

#Import packages
import pandas as pd
from sqlalchemy import create_engine, text

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
    
    #Handle csv data sources
    elif src_type == "csv":
        #Return file contents
        return pd.read_csv(settings[src])