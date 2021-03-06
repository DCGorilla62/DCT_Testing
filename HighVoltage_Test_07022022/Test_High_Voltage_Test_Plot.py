#!/bin/env python3

######################################
#    HELIX High Voltage Test Plot    #
#        Dennis H. Calderon          #
#    calderon-madera.1@osu.edu       #
######################################

#######################################################
"""
=======================
##High_Voltage_Test_Plot.py##
======================
Author: Dennis H. Calderon
Email: calderon-madera.1@osu.edu
Date: July 03, 2022
Modified: July 05, 2022
=======================
Descripiton: 
This PYTHON script will take in 2 csv files of data from the High Voltage 
testing done at Indiana Universiry on July 02, 2022. The test was done for 
both supply 1 (under load) and supply 2 (under load and no load).
Data was taken by hand (Me) for given DAC and voltage reading.
Data was saved from serial output of DAC and ADC_Voltage and ADC_Current 
for POTENTIAL supply and CATHODE supply.

The script will create plots for DAC vs other variables when it can and 
also fit a line and label the paramers when appropiate.

Note:
The files should be prepped using,
 grep | sed > filename.txt
=======================
Usage:
python High_Voltage_Test_Plot.py <filename1> <filename2>

=======================
Options:

=======================
example:
python High_Voltage_Test_Plot.py Supply_1_Load_36M_Ohm.csv large_load_HVSupply1.txt
=======================
"""

#######################################################
import timeit
start = timeit.default_timer()
#######################################################
print("\n")
print('\033[1;37m#\033[0;0m'*50)
print("Now running \033[1;4;5;31mHigh_Voltage_Test_Plot.py\033[0;0m!")
print('\033[1;37m#\033[0;0m'*50)
print('\n')
##########################################
print("\033[1;37mPlease wait patiently...\033[0;0m")
print('Importing libraries...')

##########################################
#System libraries
#import sys
import argparse
#import csv
#import types
#import os
import warnings
warnings.filterwarnings("ignore")
#print('...')

#Python libraries
import matplotlib.pyplot as plt
#from matplotlib.lines import Line2D
import numpy as np
#import pandas as pd
print('...')
##########################################

###
parser = argparse.ArgumentParser(
        description='Read filename with list of effective volume errors.')
parser.add_argument("filename", help = "Path to the file you want to use.")
parser.add_argument("filename2", help = "Path to another file you want to use.")
g = parser.parse_args()

filename = g.filename
filename2 = g.filename2

#making cleaner name from given filename
name = filename.split('/')[-1].split('.')[0]
name2 = filename2.split('/')[-1].split('.')[0]

data_dict = {'P': {'DAC': [], 'ADC_Voltage': [], 'ADC_Current': []},
                  'C': {'DAC': [], 'ADC_Voltage': [], 'ADC_Current': []},
                  'HV': {'DAC': [], 'Voltage': []}}

#Reads data from first file and appends to dictionary
with open(filename) as f:
    for line in f:
        HV = [float(value) for value in line.split(',')]
        data_dict['HV']['DAC'].append(HV[0])
        data_dict['HV']['Voltage'].append(HV[1])

#Reads data from second file and appends to dictionary        
with open(filename2) as f2:
    for line in f2:
        P = [float(value) for value in line.split()[1].split(',')]
        C = [float(value) for value in line.split()[3].split(',')]
        data_dict['P']['DAC'].append(P[0]) 
        data_dict['P']['ADC_Voltage'].append(P[1]) 
        data_dict['P']['ADC_Current'].append(P[2]) 
        data_dict['C']['DAC'].append(C[0]) 
        data_dict['C']['ADC_Voltage'].append(C[1]) 
        data_dict['C']['ADC_Current'].append(C[2]) 

import seaborn as sns

#Define a plotting function to make scatter plot and fit a line to it
def plotter(x, y, name, xlabel='x_val', ylabel='y_val', supply='HV', x_name='input', y_name='data'):
    '''
    Simple plot maker. Will make a scatter plot and 
    fit the data with numpy.polyfit()
    '''
    print("Plotting...")
    theta = np.polyfit(x, y, 1)
    y_line = theta[1] + theta[0] * np.array(x)
    res = y - y_line
    
    plt.figure(10, figsize = (8,6))
    sns.residplot(x=x, y=y_line, lowess=True, color='g')
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_RESID.png".format(name,supply,x_name,y_name),dpi=300)
    plt.clf()


    plt.figure(1, figsize = (8,6))
    plt.scatter(x, y, s=10.0)
    plt.plot(x,y_line, color='red', linewidth=1.0)
    
    plt.title("{0}".format(name))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)

    ax = plt.gca()
    plt.text(0.1,0.8, "y = {0:5.3f} x + {1:5.3f}".format(theta[0],theta[1]),
             transform = ax.transAxes, size=10, color="red")
    plt.savefig("test_plots/{0}_{1}_{2}_{3}.png".format(name,supply,x_name,y_name),dpi=300)
    plt.clf()

    # plt.figure(2, figsize=(8,6))
    # plt.scatter(x,res)
    # plt.savefig("test_plots/{0}_{1}_{2}_{3}_Res.png".format(name,supply,xlabel,ylabel),dpi=300)
    # plt.clf()
    
    # plt.figure(3, figsize=(8,6))
    # plt.hist(res)
    # plt.savefig("test_plots/{0}_{1}_{2}_{3}_Hist.png".format(name,supply,xlabel,ylabel),dpi=300)
    # plt.clf()

    # plt.figure(4, figsize=(8,6))
    # plt.hist(np.std(res))
    # plt.savefig("test_plots/{0}_{1}_{2}_{3}_Hist_Std.png".format(name,supply,xlabel,ylabel),dpi=300)
    # plt.clf()

    print("Done!")

    return

#########
##Plots##
#########

#Makes plot from 'HV' (data taken by hand)    
plotter(data_dict['HV']['DAC'], data_dict['HV']['Voltage'], 
        name, xlabel='DAC Value', ylabel='High Voltage (|V|)', 
        x_name='DAC', y_name='HighVoltage', supply='HV')

#Need a try and except block because it can't fit a line if data is 0
#Will be 0 if we weren't recording for correct supply
#Supply1 = POTENTIAL & Supply2 = CATHODE
try:
    plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Voltage'], 
            name, xlabel='DAC Value', ylabel='ADC Voltage Value', 
            x_name='DAC', y_name='ADC_Voltage', supply='P')
    plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Current'], 
            name, xlabel='DAC Value', ylabel='ADC Current Value', 
            x_name='DAC', y_name='ADC_Current', supply='P')
    
    plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Voltage'], 
            name, xlabel='DAC Value', ylabel='ADC Voltage Value', 
            x_name='DAC', y_name='ADC_Voltage', supply='C')
    plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Current'], 
            name, xlabel='DAC Value', ylabel='ADC Current Value', 
            x_name='DAC', y_name='ADC_Voltage', supply='C')
    
except ValueError:
    try:
        plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Voltage'], 
                name, xlabel='DAC Value', ylabel='ADC Voltage Value',
                x_name='DAC', y_name='ADC_Voltage', supply='P')
        plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Current'], 
                name, xlabel='DAC Value', ylabel='ADC Current Value', 
                x_name='DAC', y_name='ADC_Current', supply='P')
    except ValueError:
        try:
            plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Voltage'], 
                    name, xlabel='DAC Value', ylabel='ADC Voltage Value', 
                    x_name='DAC', y_name='ADC_Voltage', supply='C')
            plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Current'], 
                    name, xlabel='DAC Value', ylabel='ADC Current Value', 
                    x_name='DAC', y_name='ADC_Current', supply='C')
        except IndexError:
            print("Event")

##End of script##
stop = timeit.default_timer()
print('Time: \033[1;31m{0}\033[0;0m'.format(stop - start))
exit()
