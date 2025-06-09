import numpy as np
import pandas as pd
import pickle

from sklearn.metrics import mean_squared_error

def evaluate_mse(site, y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred)
    print(site, mse)
    
    return mse

def main(test_desc):
    sites = [
        "RAL01", "RAN01", "RAPNM", "RKEQ4", "RP401", "RRV03", "RRV30", "RRVNQ"]
    
    sites_mse = []

    for site in sites:

        path_prefix = "./data/sites/"
        X_test = pd.read_csv(path_prefix + site + "/x_test.csv")
        y_test= pd.read_csv(path_prefix + site + "/y_test.csv")
        model = pickle.load(open(f"./data/sites/{site}/model.sav", 'rb'))

        y_pred = model.predict(X_test)

        sites_mse.append(evaluate_mse(site, y_test, y_pred))


    # Output the evaluation results
    run_data_filename = "./output/run_data.xlsx"

    #Check the run data file exists and the next run number
    try:
        run_data = pd.read_excel(run_data_filename, sheet_name="Runs")
        run_no = len(run_data)
        mode = "a"
    except FileNotFoundError as e:
        run_no = 1
        mode = "w"

    #Get the columns and data for the run data file
    df_out_cols = ["Run", "Description"] + ["mse_" + x for x in sites]
    df_out_data = (np.array([run_no, test_desc] + sites_mse)).reshape(1, -1)
    df_out = pd.DataFrame(
        data=df_out_data, 
        columns=df_out_cols)
    
    #Write output to the runs file
    with pd.ExcelWriter(run_data_filename, mode=mode) as writer: 
        df_out.to_excel(writer, sheet_name="Runs", index=False)

description = "Base test by site"
main(description)