import toml

#Return an object containing all runtime settings
def load_settings():

    #Load toml settings from config
    config = toml.load("./config.toml")

    script_dir = config["struct"]["sql_script_dir"]

    settings = {
        #Files and directories
        "site_data_dir": config["struct"]["site_data_dir"],
        "run_tracker_file": config["struct"]["run_tracker_file"],

        #SQL Connection settings
        "sql_dsn": config["database"]["sql_dsn"],
        "sql_database": config["database"]["sql_database"],
        "sql_schema": config["database"]["sql_schema"],

        #SQL table names
        "sql_base_destination": (
            config["database"]["tables"]["sql_base_destination"]),
        "sql_preprocessing_destination": (
            config["database"]["tables"]["sql_preprocessing_destination"]),

        #Scripts to create destination tables
        "script_create_base": ("./" + script_dir + 
            config["scripts"]["create"]["script_create_base"]),
        "script_create_preprocessing": ("./" + script_dir + 
            config["scripts"]["create"]["script_create_preprocessing"]),

        #Data to pull
        "script_sfw_base_sus_spell": ("./" + script_dir +
            config["scripts"]["sfw"]["script_sfw_base_sus_spell"]),
        "script_sfw_preprocessing": ("./" + script_dir +
            config["scripts"]["sfw"]["script_sfw_preprocessing"]),

        #Hospital Sites in Scope
        "sites": config["sites"]["sites"]
    }

    return settings