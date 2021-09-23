import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    #specify path for now, implement file grab later
    workingfile = '/home/spenceryeager/Documents/calculations/chopper_data/Hour 23 1000mA.txt'
    data = pd.read_csv(workingfile, sep=',', skiprows=rowskip(workingfile))
    print(data)


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