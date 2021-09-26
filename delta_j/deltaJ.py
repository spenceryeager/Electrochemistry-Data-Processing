import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import numpy as np
import pandas as pd
import os
from tkinter import *
import tkinter.filedialog as fd
root = Tk()
root.withdraw()

def main():
    #specify path for now, implement file grab later
    # workingfile = '/home/spenceryeager/Documents/calculations/chopper_data/Hour 23 1000mA.txt'
    workingfile = fd.askopenfilename()
    global directory 
    # directory = '/home/spenceryeager/Documents/calculations/chopper_data/'
    directory = os.path.dirname(workingfile)
    print(directory)
    global data # data must be global to be called in onselect function
    data = pd.read_csv(workingfile, sep=',', skiprows=rowskip(workingfile)) 
    columns = ['Potential (V)', 'Dark Current (A)', 'On Current (A)', 'Delta Current (A)']
    global output_data # generated data will be appended to this
    output_data = pd.DataFrame(columns = columns)
    
    #Plotting
    fig, ax = plt.subplots()
    ax.plot(data['Potential/V'], data[' Current/A'], color='blue')
    ax.set_xlabel('Potential (V)')
    ax.set_ylabel('Current (A)')
    ax.set_title('Select the potential range that contains the on/off current\nClose the graph when finished selecting points')
    rectprops = dict(facecolor='blue', alpha=0.4)
    span = mwidgets.SpanSelector(ax, onselect, 'horizontal', rectprops=rectprops)
    plt.show()
    
    # Double checking selected points with graph
    plt.plot(data['Potential/V'], data[' Current/A'], color='blue')
    plt.scatter(output_data['Potential (V)'], output_data['Dark Current (A)'], label='Off Current', marker='o', color='red')
    plt.scatter(output_data['Potential (V)'], output_data['On Current (A)'], label='On Current', marker='o', color='darkorange')
    plt.title('Double check points and make sure they look reasonable')
    plt.xlabel('Potential (V)')
    plt.ylabel('Current (A)')
    plt.legend(loc='best')
    plt.show()

    filemake(output_data, directory)

def onselect(vmin, vmax):
    indmin, indmax = np.searchsorted(data['Potential/V'], (vmin, vmax))
    selection(indmin, indmax)
    # write to a CSV file for further analysis.


def selection(indmin, indmax):
    potential_array = np.array(data['Potential/V'][indmin:indmax])
    current_array = np.array(data[' Current/A'][indmin:indmax])
    dark_current = max(current_array)
    on_current = min(current_array)
    delta_current = dark_current - on_current
    inddark = np.where(current_array == dark_current)
    inddark = inddark[0][0]
    indon = np.where(current_array == on_current)
    indon = indon[0][0]
    if inddark < indon:
        medianV = np.median(potential_array[inddark:indon])
        append = [medianV, dark_current, on_current, delta_current]
        output_data.loc[len(output_data)] = append
        
    else:
        medianV = np.median(potential_array[indon:inddark])
        append = [medianV, dark_current, on_current, delta_current]
        output_data.loc[len(output_data)] = append



def filemake(data, filepath):
    outputdir = "output_data"
    output = os.path.join(filepath, outputdir)
    if not os.path.isdir(output):
        os.mkdir(output)
    filename = os.path.join(output, "selected_data.csv")
    data.to_csv(filename, sep=',')


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