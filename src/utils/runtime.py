import toml

from dotenv import load_dotenv
from os import getenv

#Return an object containing all runtime settings
def load_settings():

    #Load env settings
    load_dotenv(override=True)

    #Load toml settings from config
    config = toml.load("./config.toml")

    script_dir = config["struct"]["sql_script_dir"]

    settings = {
        #Runtime settings
        "run_description": getenv("RUN_DESCRIPTION"),
        "tail_cap_los": int(getenv("TAIL_CAP_LOS")),
        "regressor": getenv("REGRESSOR"),
        "track_run": int(getenv("TRACK_RUN")),
        "plot_performance": int(getenv("PLOT_PERFORMANCE")),
        "feature_coefficients": int(getenv("FEATURE_COEFFICIENTS")),
        "p_values": int(getenv("P_VALUES")),

        #Files and directories
        "site_data_dir": config["struct"]["site_data_dir"],
        "site_output_dir": config["struct"]["site_output_dir"],
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