import matplotlib.pyplot as plt

def plot_prediction_against_actual(test, pred):
    plt.scatter(test, pred, alpha=0.5)
    plt.plot([test.min(), test.max()], [test.min(), test.max()], 'r--')
    plt.xlabel("Actual")
    plt.ylabel("Predicted")
    plt.title("Actual vs Predicted")
    plt.show()