import toml

#Return an object containing all runtime settings
def load_settings():

    #Load toml settings from config
    config = toml.load("./config.toml")

    settings = {
        #SQL Connection settings
        "sql_dsn": config["database"]["sql_dsn"],
        "sql_database": config["database"]["sql_database"],
        "sql_destination_schema": config["database"]["sql_destination_schema"],
        "sql_destination_table": config["database"]["sql_destination_table"],
        "sql_createtable": ("./" + config["struct"]["script_dir"] + 
                            config["database"]["sql_createtable"]),

        #Data to pull
        "hrg_trim_file":    ("./" + config["struct"]["data_dir"] +
                            config["data_files"]["ds_hrg_trim"]),
        "cc_list_file":     ("./" + config["struct"]["data_dir"] +
                            config["data_files"]["ds_cc_list"]),

        "sus_spell_script": ("./" + config["struct"]["script_dir"] + 
                            config["data_scripts"]["ds_sus_spell"]),
        "sus_episode_icd_script":
                            ("./" + config["struct"]["script_dir"] + 
                            config["data_scripts"]["ds_sus_episode_icd_data"]),
        "hospital_infections_script":
                            ("./" + config["struct"]["script_dir"] + 
                            config["data_scripts"]["ds_hospital_infections"]),
        "workforce_sickness_script":
                            ("./" + config["struct"]["script_dir"] + 
                            config["data_scripts"]["ds_workforce_sickness"]),
        "workforce_vacancy_script":
                            ("./" + config["struct"]["script_dir"] + 
                            config["data_scripts"]["ds_workforce_vacancy"]),
        "beds_script":
                            ("./" + config["struct"]["script_dir"] + 
                            config["data_scripts"]["ds_beds"]),
        "medically_optimised_script":
                            ("./" + config["struct"]["script_dir"] + 
                            config["data_scripts"]["ds_mos"]),

        #Structure Information
        "hrg_trim_days_column_el": config["struct"]["hrg_trim_days_column_el"],
        "hrg_trim_days_column_nel": config["struct"]["hrg_trim_days_column_nel"]
    }

    return settings