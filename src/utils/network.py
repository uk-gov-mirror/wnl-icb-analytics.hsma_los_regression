#Functions for interacting with the database

#Import packages
import pandas as pd
from sqlalchemy import create_engine, MetaData, text, insert
from sqlalchemy.orm import sessionmaker

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
    
#Function to upload data for a given dataset
def upload_data(df, engine, settings):

    #Load destination table name
    sql_database = settings["sql_database"]
    sql_schema = settings["sql_destination_schema"]
    sql_table = settings["sql_destination_table"]

    #Upload the processed data
    batch_size = 200
    
            
    rows = df.to_dict(orient="records")

    query_exists = text(
    "SELECT * FROM sys.schemas AS s " +
    "INNER JOIN sys.tables AS t " +
    "ON s.schema_id = t.schema_id " +
    f"WHERE s.name = '{sql_schema}' "
    f"AND  t.name = '{sql_table}'"
    )

    with engine.connect() as con:
        #Set the database
        con.execute(text(f"USE {sql_database};"))

        #Check if the table already exists
        res = con.execute(query_exists)

        #If the destination table already exists then DROP it
        if len(res.fetchall()) > 0:
            #Create delete query to remove existing data for this data point
            del_query = (f"TRUNCATE TABLE "
                        f"[{sql_database}].[{sql_schema}].[{sql_table}] ")
    
            #Delete existing data from the destination
            con.execute(text(del_query))

        #Create the table
        else:
            pass
        
        #Set meta data
        metadata = MetaData(schema=sql_schema)
        metadata.reflect(bind=engine)
        sqlalc_table = metadata.tables[sql_schema + '.' + sql_table]

        #Group the data into batches and upload
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i+batch_size]
            result = con.execute(
                insert(sqlalc_table),
                batch
            )
            print(i)

        con.commit()