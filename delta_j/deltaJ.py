import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
import numpy as np
import pandas as pd

def main():
    #specify path for now, implement file grab later
    workingfile = '/home/spenceryeager/Documents/calculations/chopper_data/Hour 23 1000mA.txt'
    global directory 
    directory = '/home/spenceryeager/Documents/calculations/chopper_data/'
    global data # data must be global to be called in onselect function
    data = pd.read_csv(workingfile, sep=',', skiprows=rowskip(workingfile))
    columns = ['Potential (V)', 'Dark Current (A)', 'On Current (A)', 'Delta Current (A)']
    global data_points # generated data will be appended to this
    data_points = pd.DataFrame(columns = columns)
    
    #Plotting
    fig, ax = plt.subplots()
    ax.plot(data['Potential/V'], data[' Current/A'], color='blue')
    ax.set_xlabel('Potential (V)')
    ax.set_ylabel('Current (A)')
    ax.set_title('Select the potential range that contains the on/off current\nClose the graph when finished selecting points')
    rectprops = dict(facecolor='blue', alpha=0.4)
    span = mwidgets.SpanSelector(ax, onselect, 'horizontal', rectprops=rectprops)
    plt.show()


def onselect(vmin, vmax):
    indmin, indmax = np.searchsorted(data['Potential/V'], (vmin, vmax))
    selection(indmin, indmax)
    # take the indices here, get the max current and min current.
    # max and min should be right near where the selection was made. 
    # take the potential value @ both currents and avg them
    # write to a CSV file for further analysis.
    print(indmin, indmax)


def selection(indmin, indmax):
    potential_array = np.array(data['Potential/V'][indmin:indmax])
    current_array = np.array(data[' Current/A'][indmin:indmax])
    dark_current = max(current_array)
    on_current = min(current_array)
    inddark = np.where(current_array == dark_current)
    inddark = inddark[0][0]
    indon = np.where(current_array == on_current)
    indon = indon[0][0]
    if inddark < indon:
        # print(inddark, indon)
        medianV = np.median(potential_array[inddark:indon])
        
    else:
        medianV = np.median(potential_array[indon:inddark])
        


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