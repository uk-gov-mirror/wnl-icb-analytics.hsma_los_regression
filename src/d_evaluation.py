import numpy as np
import pandas as pd
import pickle

from datetime import datetime as dt
from sklearn.metrics import mean_squared_error

import utils.runtime as rt
import utils.evaluation_plots as ep

def evaluate_mse(site, y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred)
    print(site, mse)
    
    return mse

def main():
    #Load the runtime settings
    settings = rt.load_settings()

    test_desc = settings["run_description"]

    sites = settings["sites"]
    sites_mse = []

    for site in sites:

        path_prefix = "./" + settings["site_data_dir"] + site
        X_test = pd.read_csv(path_prefix + "/x_test.csv")
        y_test= pd.read_csv(path_prefix + "/y_test.csv")
        model = pickle.load(open(path_prefix + "/model.sav", 'rb'))

        y_pred = model.predict(X_test)

        sites_mse.append(evaluate_mse(site, y_test, y_pred))

        if (settings["feature_coefficients"]and 
            settings["regressor"] == "Poisson"):
            print(pd.DataFrame(zip(X_test.columns, model.coef_)))

        if (settings["p_values"] and 
            settings["regressor"][-2:] == "sm"):
            print(model.pvalues)


        if settings["plot_performance"]:
            ep.plot_performance(settings, site, y_test, y_pred)

        print()

    if settings["track_run"]:
        print("Recording Run Info...")
        # Output the evaluation results
        run_data_filename = "./" + settings["run_tracker_file"]

        #Check the run data file exists and the next run number
        try:
            run_data = pd.read_csv(run_data_filename)
            run_no = len(run_data) + 1
            header=False
            mode = "a"
        except FileNotFoundError as e:
            run_no = 1
            header=True
            mode = "w"

        #Get the columns and data for the run data file
        df_out_cols = (
            ["Run", "Description"] + 
            ["mse_" + x for x in sites] + 
            ["timestamp"]
        )

        df_out_data = (
            np.array(
                [run_no, test_desc] + sites_mse + [dt.today()])).reshape(1, -1)
        
        df_out = pd.DataFrame(
            data=df_out_data, 
            columns=df_out_cols)
        
        #Write output to the runs file
        df_out.to_csv(run_data_filename, header=header, mode=mode, index=False)

main()