#!/bin/env python3

######################################
#    HELIX High Voltage Test Plot    #
#        Dennis H. Calderon          #
#    calderon-madera.1@osu.edu       #
######################################

#######################################################
"""
=======================
##High_Voltage_Test_Plot_07022022.py##
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
#import warnings
#warnings.filterwarnings("ignore")
print('...')

#Python libraries
import matplotlib.pyplot as plt
#from matplotlib.lines import Line2D
import numpy as np
#import pandas as pd
import matplotlib.style as style
#style.use('tableau-colorblind10')
style.use('seaborn-colorblind')
print('...')
##########################################

###
parser = argparse.ArgumentParser(
        description='Read filename with list of effective volume errors.')
parser.add_argument("filename", help = "Path to the file you want to use.")
parser.add_argument("supply", help = "1 or 2 Supply used. Cathode: Supply 1 or Potential: Supply2.")

g = parser.parse_args()

filename = g.filename
supply = g.supply
#print(supply)
#print(type(supply))
#making cleaner name from given filename
name = filename.split('/')[-1].split('.')[0]


print(name)

print('#'*28)
print('\n')

#creating empty dictionary where I will store my data
data_dict = {'P': {'DAC_Volts': [], 'DAC_Current_Limit': [], 'ADC_Voltage': [], 'ADC_Current': []},
             'C': {'DAC_Volts': [], 'DAC_Current_Limit': [], 'ADC_Voltage': [], 'ADC_Current': []}}

#Reads data from second file and appends to dictionary        
with open(filename) as f:
    for line in f:
        P = [float(value) for value in line.split()[1].split(',')]
        # print(P)
        # exit()
        C = [float(value) for value in line.split()[3].split(',')]
        data_dict['P']['DAC_Volts'].append(P[0])
        data_dict['P']['DAC_Current_Limit'].append(P[1]) 
        data_dict['P']['ADC_Voltage'].append(P[2]) 
        data_dict['P']['ADC_Current'].append(P[3]) 
        data_dict['C']['DAC_Volts'].append(C[0])
        data_dict['C']['DAC_Current_Limit'].append(C[1]) 
        data_dict['C']['ADC_Voltage'].append(C[2]) 
        data_dict['C']['ADC_Current'].append(C[3]) 

#print(data_dict)
# exit()


        
#Define a plotting function to make scatter plot and fit a line to it
def plotter(x, y, name, xlabel='x_val', ylabel='y_val', supply='HV', x_name='input', y_name='data'):
    '''
    Simple plot maker. Will make a scatter plot and 
    fit the data with numpy.polyfit()
    '''
    
    #
    print("Plotting...")
    x = np.array(x)
    y = np.array(y)
    # print(x,y)
    theta = np.polyfit(x, y, 1)
    y_line = theta[1] + theta[0] * x
    res = y - y_line
    #vprint(res)
    
    plt.figure(1, figsize = (8,6))
    plt.scatter(x, y, s=10.0)
    plt.plot(x,y_line, color='red', linewidth=1.0)
    plt.title("{0}".format(name))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5)
    ax = plt.gca()
    plt.text(0.1,0.8, "y = {0:5.3f} x + {1:5.3f}".format(theta[0],theta[1]),
             transform = ax.transAxes, size=10, color="red")
    plt.savefig("test_plots/{0}_{1}_{2}_{3}.png".format(name,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    plt.figure(2, figsize=(8,6))
    plt.scatter(x, res, s=10.0)
    plt.plot(x,np.zeros(len(x)), color='red', linewidth=1.0, linestyle='-')
    plt.title("Residuals_{0}".format(name))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_Res.png".format(name,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    plt.figure(3, figsize=(8,6))
    plt.hist(res)#, histtype='step')
    plt.title("Hist_Residuals_{0}".format(name))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel('Counts', labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_Hist.png".format(name,supply,x_name,y_name),dpi=300)
    plt.clf()

    ##masked##
    #interior#

    index_int  = np.where( (np.array(x) > 90) & (np.array(x) < 4000) ) 
    x_int = x[index_int]
    y_int = y[index_int]

    # x = np.array(x)
    # y = np.array(y)
    # index = np.where( (x > 10) & (x < 4010) )
    # x = x[index]
    # y = y[index]
    name_int = 'Masked_Interior_'+name


    theta_int = np.polyfit(x_int, y_int, 1)
    y_line_int = theta_int[1] + theta_int[0] * x_int
    res_int = y_int - y_line_int

    plt.figure(1, figsize = (8,6))
    plt.scatter(x_int, y_int, s=10.0)
    plt.plot(x_int,y_line_int, color='red', linewidth=1.0)
    plt.title("{0}".format(name))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5)
    ax = plt.gca()
    plt.text(0.1,0.8, "y = {0:5.3f} x + {1:5.3f}".format(theta_int[0],theta_int[1]),
             transform = ax.transAxes, size=10, color="red")
    plt.savefig("test_plots/{0}_{1}_{2}_{3}.png".format(name_int,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    plt.figure(2, figsize=(8,6))
    plt.scatter(x_int, res_int, s=10.0)
    plt.plot(x_int,np.zeros(len(x_int)), color='red', linewidth=1.0, linestyle='-')
    plt.title("Residuals_{0}".format(name))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_Res.png".format(name_int,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    plt.figure(3, figsize=(8,6))
    plt.hist(res_int)#, histtype='step')
    plt.title("Hist_Residuals_{0}".format(name))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel('Counts', labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_Hist.png".format(name_int,supply,x_name,y_name),dpi=300)
    plt.clf()

    #Exclude end only
    #interior#

    index_excl  = np.where( (np.array(x) < 4000) ) 
    x_excl = x[index_excl]
    y_excl = y[index_excl]

    # x = np.array(x)
    # y = np.array(y)
    # index = np.where( (x > 10) & (x < 4010) )
    # x = x[index]
    # y = y[index]
    name_excl = 'Masked_Exclude_'+name

    theta_excl = np.polyfit(x_excl, y_excl, 1)
    y_line_excl = theta_excl[1] + theta_excl[0] * x_excl
    res_excl = y_excl - y_line_excl

    plt.figure(1, figsize = (8,6))
    plt.scatter(x_excl, y_excl, s=10.0)
    plt.plot(x_excl,y_line_excl, color='red', linewidth=1.0)
    plt.title("{0}".format(name))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5)
    ax = plt.gca()
    plt.text(0.1,0.8, "y = {0:5.3f} x + {1:5.3f}".format(theta_excl[0],theta_excl[1]),
             transform = ax.transAxes, size=10, color="red")
    plt.savefig("test_plots/{0}_{1}_{2}_{3}.png".format(name_excl,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    plt.figure(2, figsize=(8,6))
    plt.scatter(x_excl, res_excl, s=10.0)
    plt.plot(x_excl,np.zeros(len(x_excl)), color='red', linewidth=1.0, linestyle='-')
    plt.title("Residuals_{0}".format(name))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_Res.png".format(name_excl,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    plt.figure(3, figsize=(8,6))
    plt.hist(res_excl)#, histtype='step')
    plt.title("Hist_Residuals_{0}".format(name))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel('Counts', labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_Hist.png".format(name_excl,supply,x_name,y_name),dpi=300)
    plt.clf()

    
    print("Done!")
        
    # #Mega Plot
    # if supply=='HV':
    #     plt.figure(1, figsize = (8,6))
    #     plt.scatter(x, y, s=10.0)
    #     plt.plot(x,y_line, linestyle='dotted', linewidth=1.0, label='All')
    #     plt.plot(x_excl,y_line_excl, linestyle='dashdot', linewidth=1.0, label='Exlcude')
    #     plt.plot(x_int,y_line_int, linestyle='dashed', linewidth=1.0, label='Interior')
    #     plt.plot(x,2.4353*x, linestyle='solid', linewidth=1.0, label='Theoretical')
    #     plt.title("{0}".format(name))
    #     plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    #     plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    #     plt.legend()
    #     plt.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5)
    #     ax = plt.gca()
    #     plt.savefig("test_plots/All_Fits_{0}_{1}_{2}_{3}.png".format(name,supply,x_name,y_name),dpi=300)
    #     plt.clf()
        
    #     plt.figure(1, figsize = (8,6))
    #     plt.scatter(x, y, s=10.0)
    #     plt.plot(x,y_line, linestyle='dotted', linewidth=1.0, label='All')
    #     plt.plot(x_excl,y_line_excl, linestyle='dashdot', linewidth=1.0, label='Exclude')
    #     plt.plot(x_int,y_line_int, linestyle='dashed', linewidth=1.0, label='Interior')
    #     plt.plot(x,2.4353*x, linestyle='solid', linewidth=1.0, label='Theoretical')
        
    #     # left, right = xlim()  # return the current xlim
    #     # xlim((left, right))   # set the xlim to left, right
    #     # xlim(left, right)     # set the xlim to left, right
        
    #     # If you do not specify args, you can pass left or right as kwargs, i.e.:
        
    #     #     xlim(right=3)  # adjust the right leaving left unchanged
    #     #     xlim(left=1)  # adjust the left leaving right unchanged
        
    #     # bottom, top = ylim()  # return the current ylim
    #     # ylim((bottom, top))   # set the ylim to bottom, top
    #     # ylim(bottom, top)     # set the ylim to bottom, top
    #     left, right = plt.xlim()
    #     top, bottom = plt.ylim()
    #     # plt.xlim(3500,4100)#left=3800)
    #     # plt.ylim(8000,10000)#bottom=8000)
    #     plt.xlim(left*0.8, right)
    #     plt.ylim(top, bottom*0.8)
    #     plt.title("{0}".format(name))
    #     plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    #     plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    #     plt.legend()
    #     plt.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5)
    #     ax = plt.gca()
    #     plt.savefig("test_plots/Zoom_All_Fits_{0}_{1}_{2}_{3}.png".format(name,supply,x_name,y_name),dpi=300)
    #     plt.clf()
        
        # plt.figure(4, figsize=(8,6))
        # plt.hist(np.std(res))
        # plt.savefig("test_plots/{0}_{1}_{2}_{3}_Hist_Std.png".format(name,supply,xlabel,ylabel),dpi=300)
        # plt.clf()
    
    return

# #Masked
# def masked_plotter(x, y, name, xlabel='x_val', ylabel='y_val', supply='HV', x_name='input', y_name='data'):
#     '''
#     Simple plot maker. Will make a scatter plot and 
#     fit the data with numpy.polyfit()
#     '''
#     # print(np.where((a > 2) & (a < 6) | (a == 7), -1, 100))
#     print("Plotting...")
#     x = np.array(x)
#     y = np.array(y)
#     index = np.where( (x > 10) & (x < 4010) )
#     x = x[index]
#     y = y[index]
#     name = name+'_masked'
    
#     theta = np.polyfit(x, y, 1)
#     y_line = theta[1] + theta[0] * np.array(x)
#     res = y - y_line
#     #vprint(res)
    
#     plt.figure(1, figsize = (8,6))
#     plt.scatter(x, y, s=10.0)
#     plt.plot(x,y_line, color='red', linewidth=1.0)
#     plt.title("{0}".format(name))
#     plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
#     plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
#     plt.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5)
#     ax = plt.gca()
#     plt.text(0.1,0.8, "y = {0:5.3f} x + {1:5.3f}".format(theta[0],theta[1]),
#              transform = ax.transAxes, size=10, color="red")
#     plt.savefig("test_plots/{0}_{1}_{2}_{3}.png".format(name,supply,x_name,y_name),dpi=300)
#     plt.clf()
    
#     plt.figure(2, figsize=(8,6))
#     plt.scatter(x, res, s=10.0)
#     plt.plot(x,np.zeros(len(x)), color='red', linewidth=1.0, linestyle='-')
#     plt.title("Residuals_{0}".format(name))
#     plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
#     plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
#     plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
#     plt.savefig("test_plots/{0}_{1}_{2}_{3}_Res.png".format(name,supply,x_name,y_name),dpi=300)
#     plt.clf()
    
#                             # plt.hist(data_dict[source]['{0}_1'.format(hist_var)], 
#                             #      weights=data_dict[source]['weight'], bins=bindistance, density=False, 
#                             #      histtype='step', color=color, ls='--', label=str(source)+' refracted')

#     plt.figure(3, figsize=(8,6))
#     plt.hist(res)#, histtype='step')
#     plt.title("Hist_Residuals_{0}".format(name))
#     plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
#     plt.ylabel('Counts', labelpad = 0.5, fontsize = 10)
#     plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
#     plt.savefig("test_plots/{0}_{1}_{2}_{3}_Hist.png".format(name,supply,x_name,y_name),dpi=300)
#     plt.clf()
    
#     print("Done!")
        
#     # plt.figure(4, figsize=(8,6))
#     # plt.hist(np.std(res))
#     # plt.savefig("test_plots/{0}_{1}_{2}_{3}_Hist_Std.png".format(name,supply,xlabel,ylabel),dpi=300)
#     # plt.clf()
    
#     return

#########
##Plots##
#########
#def plotter(x, y, name, xlabel='x_val', ylabel='y_val', supply='HV', x_name='input', y_name='data'):

if g.supply == 'Cathode':
    plotter(data_dict['C']['DAC_Volts'], data_dict['C']['ADC_Voltage'], 
            name='Cathode_Supply_No_Load_07222022', xlabel='DAC Volts', ylabel='Voltage (ADC Code)', 
            x_name='DAC_Volts', y_name='ADC_Voltage', supply='Cathode')
    plotter(data_dict['C']['DAC_Volts'], data_dict['C']['ADC_Current'], 
            name='Cathode_Supply_No_Load_07222022', xlabel='DAC Volts', ylabel='Current (ADC Code)', 
            x_name='DAC_Volts', y_name='ADC_Curent', supply='Cathode')
    plotter(data_dict['C']['ADC_Voltage'], data_dict['C']['ADC_Current'], 
            name='Cathode_Supply_No_Load_07222022', xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
            x_name='ADC_Voltage', y_name='ADC_Current', supply='Same_Cathode')
    
    #different supplies
    plotter(data_dict['C']['DAC_Volts'], data_dict['P']['ADC_Voltage'], 
            name='Cathode_Supply_No_Load_07222022', xlabel='DAC Volts', ylabel='Voltage (ADC Code)', 
            x_name='DAC_Volts', y_name='ADC_Current', supply='Both_Cathode')
    plotter(data_dict['C']['DAC_Volts'], data_dict['P']['ADC_Current'], 
            name='Cathode_Supply_No_Load_07222022', xlabel='DAC Volts', ylabel='Current (ADC Code)', 
            x_name='DAC_Volts', y_name='ADC_Current', supply='Both_Cathode')

elif g.supply == 'Potential':
    plotter(data_dict['P']['DAC_Volts'], data_dict['P']['ADC_Voltage'], 
            name='Potential_Supply_No_Load_07222022', xlabel='DAC Volts', ylabel='Voltage (ADC Code)', 
            x_name='DAC_Volts', y_name='ADC_Voltage', supply='Potential')
    plotter(data_dict['P']['DAC_Volts'], data_dict['P']['ADC_Current'], 
            name='Potential_Supply_No_Load_07222022', xlabel='DAC Volts', ylabel='Current (ADC Code)', 
            x_name='DAC_Volts', y_name='ADC_Curent', supply='Potential')
    plotter(data_dict['P']['ADC_Voltage'], data_dict['P']['ADC_Current'], 
            name='Potential_Supply_No_Load_07222022', xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
            x_name='ADC_Voltage', y_name='ADC_Current', supply='Same_Potential')
    
    #different supplies
    plotter(data_dict['P']['DAC_Volts'], data_dict['C']['ADC_Voltage'], 
            name='Potential_Supply_No_Load_07222022', xlabel='DAC Volts', ylabel='Voltage (ADC Code)', 
            x_name='DAC_Volts', y_name='ADC_Current', supply='Both_Potential')
    plotter(data_dict['P']['DAC_Volts'], data_dict['C']['ADC_Current'], 
            name='Potential_Supply_No_Load_07222022', xlabel='DAC Volts', ylabel='Current (ADC Code)', 
            x_name='DAC_Volts', y_name='ADC_Current', supply='Both_Potential')


stop = timeit.default_timer()
print('Time: \033[1;31m{0}\033[0;0m'.format(stop - start))
exit()

# #
# print("DAC vs ADC")
# try:
#     plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Voltage'], 
#             name, xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
#             x_name='DAC', y_name='ADC_Voltage', supply='P')
#     plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Current'], 
#             name, xlabel='DAC Code', ylabel='Curent (ADC Code)', 
#             x_name='DAC', y_name='ADC_Current', supply='P')
    
#     plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Voltage'], 
#             name, xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
#             x_name='DAC', y_name='ADC_Voltage', supply='C')
#     plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Current'], 
#             name, xlabel='DAC Code', ylabel='Current (ADC Code)', 
#             x_name='DAC', y_name='ADC_Voltage', supply='C')
#     print('\n')

# except:# ValueError:
#     try:
#         print('P')
#         plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Voltage'], 
#                 name, xlabel='DAC Code', ylabel='Voltage (ADC Code)',
#                 x_name='DAC', y_name='ADC_Voltage', supply='P')
#         plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Current'], 
#                 name, xlabel='DAC Code', ylabel='Current (ADC Code)', 
#                 x_name='DAC', y_name='ADC_Current', supply='P')
#     except:# ValueError:
#         try:
#             print('C')
#             plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Voltage'], 
#                     name, xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
#                     x_name='DAC', y_name='ADC_Voltage', supply='C')
#             plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Current'], 
#                     name, xlabel='DAC Code', ylabel='Current (ADC Code)', 
#                     x_name='DAC', y_name='ADC_Current', supply='C')
#         except:
#             print("Failed")
#             #IndexError:
#             #print("Event")
# print('\n')

# #Same supply ADC Volt vs ADC Current
# print('Same')
# print('ADC vs ADC')

# try:
#     plotter(data_dict['C']['ADC_Voltage'], data_dict['C']['ADC_Current'], 
#             name, xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
#             x_name='ADC_Voltage', y_name='ADC_Current', supply='Same_C')
#     # plotter(data_dict['C']['ADC_Voltage'], data_dict['C']['ADC_Current'], 
#     #         name, xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
#     #         x_name='ADC_Voltage', y_name='ADC_Current', supply='Same_C')
# except:
#     #print("Failed")
#     plotter(data_dict['P']['ADC_Voltage'], data_dict['P']['ADC_Current'], 
#             name, xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
#             x_name='ADC_Voltage', y_name='ADC_Current', supply='Same_P')
#     # plotter(data_dict['P']['ADC_Voltage'], data_dict['P']['ADC_Current'], 
#     #         name, xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
#     #         x_name='ADC_Voltage', y_name='ADC_Current', supply='P')
# print('\n')

#Different Supplies
print('Different Supplies')
print('ADC vs ADC')

try:
    # plotter(data_dict['C']['ADC_Voltage'], data_dict['P']['ADC_Current'], 
    #         name, xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
    #         x_name='ADC_Voltage', y_name='ADC_Current', supply='Both')
    # plotter(data_dict['P']['ADC_Voltage'], data_dict['C']['ADC_Current'], 
    #         name, xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
    #         x_name='ADC_Voltage', y_name='ADC_Current', supply='Both')

    plotter(data_dict['P']['DAC'], data_dict['C']['ADC_Voltage'], 
            name, xlabel='P: DAC Code', ylabel='C: Voltage (ADC Code)', 
            x_name='DAC', y_name='ADC_Voltage', supply='Both_P')
    plotter(data_dict['C']['DAC'], data_dict['P']['ADC_Voltage'], 
            name, xlabel='C: DAC Code', ylabel='P: Voltage (ADC Code)', 
            x_name='DAC', y_name='ADC_Voltage', supply='Both_C')

except:
    try:
        # plotter(data_dict['P']['ADC_Voltage'], data_dict['C']['ADC_Current'], 
        #         name, xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
        #         x_name='ADC_Voltage', y_name='ADC_Current', supply='Both')
        plotter(data_dict['P']['DAC'], data_dict['C']['ADC_Voltage'], 
                name, xlabel='P: DAC Code)', ylabel='C: Voltage (ADC Code)', 
                x_name='DAC', y_name='ADC_Voltage', supply='Both_P')
    except:
        plotter(data_dict['C']['DAC'], data_dict['P']['ADC_Voltage'], 
                name, xlabel='C: DAC Code', ylabel='P: Voltage (ADC Code)', 
                x_name='DAC', y_name='ADC_Voltage', supply='Both_C')
        # plotter(data_dict['C']['ADC_Voltage'], data_dict['P']['ADC_Current'], 
        #         name, xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
        #         x_name='ADC_Voltage', y_name='ADC_Current', supply='Both')
print('\n')        
#    print("Failed")

################
##Masked Plots##
################

# #Makes plot from 'HV' (data taken by hand)    
# masked_plotter(data_dict['HV']['DAC'], data_dict['HV']['Voltage'], 
#         name, xlabel='DAC Code', ylabel='High Voltage Output (|V|)', 
#         x_name='DAC', y_name='HighVoltage', supply='HV')


# try:
#     masked_plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Voltage'], 
#             name, xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
#             x_name='DAC', y_name='ADC_Voltage', supply='P')
#     masked_plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Current'], 
#             name, xlabel='DAC Code', ylabel='Curent (ADC Code)', 
#             x_name='DAC', y_name='ADC_Current', supply='P')
    
#     masked_plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Voltage'], 
#             name, xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
#             x_name='DAC', y_name='ADC_Voltage', supply='C')
#     masked_plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Current'], 
#             name, xlabel='DAC Code', ylabel='Current (ADC Code)', 
#             x_name='DAC', y_name='ADC_Voltage', supply='C')

# except:# ValueError:
#     try:
#         masked_plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Voltage'], 
#                 name, xlabel='DAC Code', ylabel='Voltage (ADC Code)',
#                 x_name='DAC', y_name='ADC_Voltage', supply='P')
#         masked_plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Current'], 
#                 name, xlabel='DAC Code', ylabel='Current (ADC Code)', 
#                 x_name='DAC', y_name='ADC_Current', supply='P')
#     except:# ValueError:
#         try:
#             masked_plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Voltage'], 
#                     name, xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
#                     x_name='DAC', y_name='ADC_Voltage', supply='C')
#             masked_plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Current'], 
#                     name, xlabel='DAC Code', ylabel='Current (ADC Code)', 
#                     x_name='DAC', y_name='ADC_Current', supply='C')
#         except:
#             #IndexError:
#             print("Event")


#print(name+'_Masked')
# ##Masked##
# index_P = np.where(np.array(data_dict['P']['DAC']) < 4000)
# # index_C = np.where(data_dict['C']['DAC'] < 4000)
# # index_HV = np.where(data_dict['HV']['DAC'] < 4000)
# # plt.scatter(np.array(Adist_0)[np.where( (Adepth > 4000) & (Adepth <= 4200) )], np.cos(np.array(Atheta_rec_0)[np.where( (Adepth > 4000) & (Adepth <= 4200) )]), s=1.0, alpha=0.25)#, color='indigo')
# print(index_P)
# print(np.array(data_dict['P']['DAC'])[index_P])
# exit()

# try:
#     plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Voltage'], 
#             name, xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
#             x_name='DAC', y_name='ADC_Voltage', supply='P')
#     plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Current'], 
#             name, xlabel='DAC Code', ylabel='Curent (ADC Code)', 
#             x_name='DAC', y_name='ADC_Current', supply='P')
    
#     plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Voltage'], 
#             name, xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
#             x_name='DAC', y_name='ADC_Voltage', supply='C')
#     plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Current'], 
#             name, xlabel='DAC Code', ylabel='Current (ADC Code)', 
#             x_name='DAC', y_name='ADC_Voltage', supply='C')
    
# except:# ValueError:
#     try:
#         plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Voltage'], 
#                 name, xlabel='DAC Code', ylabel='Voltage (ADC Code)',
#                 x_name='DAC', y_name='ADC_Voltage', supply='P')
#         plotter(data_dict['P']['DAC'], data_dict['P']['ADC_Current'], 
#                 name, xlabel='DAC Code', ylabel='Current (ADC Code)', 
#                 x_name='DAC', y_name='ADC_Current', supply='P')
#     except:# ValueError:
#         try:
#             plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Voltage'], 
#                     name, xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
#                     x_name='DAC', y_name='ADC_Voltage', supply='C')
#             plotter(data_dict['C']['DAC'], data_dict['C']['ADC_Current'], 
#                     name, xlabel='DAC Code', ylabel='Current (ADC Code)', 
#                     x_name='DAC', y_name='ADC_Current', supply='C')
#         except:
#             #IndexError:
#             print("Event")

##End of script##
stop = timeit.default_timer()
print('Time: \033[1;31m{0}\033[0;0m'.format(stop - start))
exit()
