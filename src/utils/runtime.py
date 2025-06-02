import toml

#Return an object containing all runtime settings
def load_settings():

    #Load toml settings from config
    config = toml.load("./config.toml")

    settings = {
        #SQL Connection settings
        "sql_dsn": config["database"]["sql_dsn"],
        "sql_database": config["database"]["sql_database"],
        "sql_schema": config["database"]["sql_schema"],

        #SQL table names
        "sql_pull_destination": (
            config["database"]["tables"]["sql_pull_destination"]),

        #Scripts to create destination tables
        "script_pull_create": ("./" + config["struct"]["script_dir"] + 
                            config["scripts"]["create"]["script_pull_create"]),

        #Data to pull
        "script_pull_source":    ("./" + config["struct"]["script_dir"] +
                            config["scripts"]["sfw"]["script_pull_source"]),
    }

    return settings