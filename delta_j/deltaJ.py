import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import numpy as np
import pandas as pd

def main():
    #specify path for now, implement file grab later
    workingfile = '/home/spenceryeager/Documents/calculations/chopper_data/Hour 23 1000mA.txt'
    data = pd.read_csv(workingfile, sep=',', skiprows=rowskip(workingfile))
    fig, ax = plt.subplots()
    ax.plot(data['Potential/V'], data[' Current/A'], color='blue')
    rectprops = dict(facecolor='blue', alpha=0.4)
    span = mwidgets.SpanSelector(ax, onselect, 'horizontal', rectprops=rectprops)
    plt.show()


def onselect(vmin, vmax):
    global max_compval
    global min_compval
    max_compval = vmax
    min_compval = vmin


def rowskip(working_file):
    file = open(working_file, 'r')
    count = 0
    for line in file:
        if line.strip() == "Potential/V, Current/A":
            row = count
        count += 1
    return row


if __name__ == "__main__":
    main()