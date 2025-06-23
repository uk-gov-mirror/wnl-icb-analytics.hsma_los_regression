import matplotlib.pyplot as plt

def plot_performance(settings, site, y_test, y_pred, 
                     title="prediction_performance"):
    #Plot actuals against residuals
    plt.clf()
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.xlabel("Actual LoS")
    plt.ylabel("Predicted LoS")
    plt.title("Actual vs Predicted LoS:" + site)
    
    output_dir = "./" + settings["site_output_dir"]
    plt.savefig(f"{output_dir}{site}/{title}.png")