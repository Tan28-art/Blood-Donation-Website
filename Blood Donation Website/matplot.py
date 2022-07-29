import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt


plt.title("Visual Representation of Blood Types")

y_axis = [0.36, 1.11, 1.99, 2.55, 5.88, 22.02, 27.42, 38.67]
x_axis = ["AB-", "B-", "A-", "O-", "AB+", "B+", "A+", "O+"]
# explode = [0, 0, 0, 0.1, 0, 0, 0, 0]
colors = [
    "#22070e",
    "#881b38",
    "#aa2246",
    "#cc2854",
    "#d83b65",
    "#e16686",
    "#e788a1",
    "#eeaabc",
    "#f5ccd7",
]

def save_graph():
    plt.bar(x_axis, y_axis, color='#d83b65', label="Blood Types")
    plt.xlabel("Blood Types")
    plt.ylabel("Percentage")
    plt.tight_layout()
    plt.savefig(r"./static/Assets/bar_graph.png")

def remove_file():
    #remove file using os module
    import os
    os.remove(r"./static/Assets/bar_graph.png")