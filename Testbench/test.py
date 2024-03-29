#!/bin/env python3

######################################
#    HELIX High Voltage Test Plot    #
#        Dennis H. Calderon          #
#    calderon-madera.1@osu.edu       #
######################################

#######################################################
"""
=======================
##test.py##
======================
Author: Dennis H. Calderon
Email: calderon-madera.1@osu.edu
Date: July 26, 2022
Modified: 
=======================
Descripiton: 

Note:
The files should be prepped using,
 grep | sed > filename.txt
=======================
Usage:

=======================
Options:

=======================
example:

=======================
"""

#######################################################
import timeit
start = timeit.default_timer()
#######################################################
script_name = 'test'
print("\n")
print('\033[1;37m#\033[0;0m'*50)
print("Now running \033[1;4;5;31m{0}\033[0;0m!".format(script_name))
print('\033[1;37m#\033[0;0m'*50)
print('\n')
##########################################
print("\033[1;37mPlease wait patiently...\033[0;0m")
print('Importing libraries...')

##########################################
#System libraries
#import sys
import argparse
import csv
#import types
#import os
#import warnings
#warnings.filterwarnings("ignore")
print('...')

#Python libraries
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import matplotlib.style as style
#style.use('tableau-colorblind10')
style.use('seaborn-colorblind')
print('...')

#Other
from test_hv_conversions import *
##########################################

# ###
# parser = argparse.ArgumentParser(
#         description='Read filename with list of effective volume errors.')
# parser.add_argument("filename", help = "Path to the file you want to use.")
# # parser.add_argument("supply", help = "1 or 2 Supply used. Cathode: Supply 1 or Potential: Supply2.")

# # parser.add_argument("source_1", help = "Path to the AraSim file you want to use.", nargs='+')
# # for above parser, could give a list of files
# # user needs to know which file  corresponds to which data set

# g = parser.parse_args()

# filename = g.filename
# # supply = g.supply
# #print(supply)
# #print(type(supply))
# #making cleaner name from given filename
# name = filename.split('/')[-1].split('.')[0]


# print(name)

print('#'*28)
print('\n')

###
'''
making different dictionary making functions for the different data 
'''
###

#funtion for creating dictionary from HV test on 07022022
def creator_0702(filename, filename2):
    '''
    '''
    #creating empty dictionary where I will store my data
    
    data_dict = {'P': {'DAC': [], 'ADC_Voltage': [], 'ADC_Current': []},
                  'C': {'DAC': [], 'ADC_Voltage': [], 'ADC_Current': []},
                  'HV': {'DAC': [], 'Voltage': []}}
    
    #read in file
    with open(filename) as f:
        
        #read line by line
        for line in f:
            
            #splitting line into values
            P = [float(value) for value in line.split()[1].split(',')]
            C = [float(value) for value in line.split()[3].split(',')]

            data_dict['P']['DAC'].append(P[0]) 
            data_dict['P']['ADC_Voltage'].append(P[1]) 
            data_dict['P']['ADC_Current'].append(P[2]) 
            data_dict['C']['DAC'].append(C[0]) 
            data_dict['C']['ADC_Voltage'].append(C[1]) 
            data_dict['C']['ADC_Current'].append(C[2]) 

    with open(filename2) as f2:
        for line in f2:
            HV = [float(value) for value in line.split(',')]
            data_dict['HV']['DAC'].append(HV[0])
            data_dict['HV']['Voltage'].append(HV[1])
            
    return data_dict

#funtion for creating dictionary from HV test on 07222022
def creator_0722(filename):
    '''
    '''
    #creating empty dictionary where I will store my data
    data_dict = {'P': {'DAC_Volts': [], 'DAC_Current_Limit': [], 'ADC_Voltage': [], 'ADC_Current': []},
                 'C': {'DAC_Volts': [], 'DAC_Current_Limit': [], 'ADC_Voltage': [], 'ADC_Current': []}}
    
    #read in file
    with open(filename) as f:
        
        #read line by line
        for line in f:
            
            #splitting line into values
            P = [float(value) for value in line.split()[1].split(',')]
            C = [float(value) for value in line.split()[3].split(',')]
            
            data_dict['P']['DAC_Volts'].append(P[0])
            data_dict['P']['DAC_Current_Limit'].append(P[1]) 
            data_dict['P']['ADC_Voltage'].append(P[2]) 
            data_dict['P']['ADC_Current'].append(P[3]) 
            data_dict['C']['DAC_Volts'].append(C[0])
            data_dict['C']['DAC_Current_Limit'].append(C[1]) 
            data_dict['C']['ADC_Voltage'].append(C[2]) 
            data_dict['C']['ADC_Current'].append(C[3]) 
            
    return data_dict

# import collections

def creator_payload(filename):
    data_dict = {}
    df = pd.read_csv(filename)
    # print(df)
    data_dict = df.to_dict(orient="list")
    #with open(filename) as f:
    #data_dict = pd.read_csv(filename,header=0).to_dict()

    #None).to_dict()#, index_col=0, squeeze=True).to_dict()
    # print(dict_from_csv)
    
    # with open(filename) as f:
    #     reader = csv.reader(f)
    #     data_dict = {rows[0]:rows[1] for rows in reader}


    return data_dict

'''
all my functions to make dictionaires work
'''



# x = creator_payload(filename)
# print(x)    


    
# # with open(filename) as f:
#     #     reader = csv.DictReader(f)#, skipinitialspace=True)

#     #     for line in reader:
#     #         print(line)
            
#     # return reader

# dict_cat = creator_payload(g.filename)
# # dict_cat
# print(dict_cat)


# dict_from_csv = {}

# with open('csv_file.csv', mode='r') as inp:
#     reader = csv.reader(inp)
#     dict_from_csv = {rows[0]:rows[1] for rows in reader}

# print(dict_from_csv)




# import pandas as pd

# dict_from_csv = pd.read_csv('csv_file.csv', header=None, index_col=0, squeeze=True).to_dict()
# print(dict_from_csv)

# exit()

        
#Define a plotting function to make scatter plot and fit a line to it
def plotter(x, y, name, title='title', xlabel='x_val', ylabel='y_val', supply='HV', x_name='input', y_name='data'):
    '''
    Simple plot maker. Will make a scatter plot and 
    fit the data with numpy.polyfit()
    '''
    
    #
    print("Plotting...")
    x = np.array(x)
    y = np.array(y)
    theta = np.polyfit(x, y, 1)
    y_line = theta[1] + theta[0] * x
    res = y - y_line
    x_lin = np.linspace(max(x),min(x),1000)
    y_all = theta[1] + theta[0] * x_lin

    plt.figure(1, figsize = (8,6))
    plt.scatter(x, y, s=10.0, color='blue', marker='D')
    plt.plot(x_lin,y_all, color='blue', linewidth=1.0)
    plt.title("{0}".format(title))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5)
    ax = plt.gca()
    plt.text(0.1,0.8, "y = {0:5.3f} x + {1:5.3f}".format(theta[0],theta[1]),
             transform = ax.transAxes, size=14, color="black")
    plt.savefig("test_plots/{0}_{1}_{2}_{3}.png".format(name,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    plt.figure(2, figsize=(8,6))
    plt.scatter(x, res, s=10.0)
    plt.plot(x,np.zeros(len(x)), color='red', linewidth=1.0, linestyle='-')
    plt.title("Residuals_{0}".format(title))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_Res.png".format(name,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    plt.figure(3, figsize=(8,6))
    plt.hist(res)#, histtype='step')
    plt.title("Hist_Residuals_{0}".format(title))
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
    plt.title("{0}".format(title))
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
    plt.title("Residuals_{0}".format(title))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_Res.png".format(name_int,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    plt.figure(3, figsize=(8,6))
    plt.hist(res_int)#, histtype='step')
    plt.title("Hist_Residuals_{0}".format(title))
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
    plt.title("{0}".format(title))
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
    plt.title("Residuals_{0}".format(title))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_Res.png".format(name_excl,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    plt.figure(3, figsize=(8,6))
    plt.hist(res_excl)#, histtype='step')
    plt.title("Hist_Residuals_{0}".format(title))
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
    #     plt.title("{0}".format(title))
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
    #     plt.title("{0}".format(title))
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
    
    return theta

def payload_plotter(x, y, name, title='title', xlabel='x_val', ylabel='y_val', supply='HV', x_name='input', y_name='data'):
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
    plt.title("{0}".format(title))
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
    plt.title("Residuals_{0}".format(title))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_Res.png".format(name,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    plt.figure(3, figsize=(8,6))
    plt.hist(res)#, histtype='step')
    plt.title("Hist_Residuals_{0}".format(title))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel('Counts', labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both',linestyle='--', linewidth=0.5)
    plt.savefig("test_plots/{0}_{1}_{2}_{3}_Hist.png".format(name,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    print('Done!')
    return theta



#########
##Plots##
#########
# diretory = '/users/PAS0654/dcalderon/Research/HELIX/DCT_Testing/data/'
directory = '../data/'

###DATA###
#Loading files and stupid

##Large Load
#Cathode
data_0702_LC = creator_0702(directory+'Indiana_07022022/Cathode_Large_Load_07022022.txt',directory+'Indiana_07022022/Cathode_HV_Large_07022022.csv')

#Potential
data_0702_LP = creator_0702(directory+'Indiana_07022022/Potential_Large_Load_07022022.txt',directory+'Indiana_07022022/Potential_HV_Large_07022022.csv')

##Small Load
#Potential
data_0702_SC = creator_0702(directory+'Indiana_07022022/Cathode_Small_Load_07022022.txt', directory+'Indiana_07022022/Cathode_HV_Small_07022022.csv')

##No Load
data_payload = creator_payload(directory+'Chicago_07202022/payload_data.txt')

data_0722_C = creator_0722(directory+'Indiana_07222022/Cathode_No_Load_07222022.txt')

data_0722_P = creator_0722(directory+'Indiana_07222022/Potential_No_Load_07222022.txt')

data_0702_NP = creator_0702(directory+'Indiana_07022022/Potential_No_Load_07022022.txt', directory+'Indiana_07022022/Potential_HV_None_07022022.csv')


##End dictionary making
stop = timeit.default_timer()
print('Time: \033[1;31m{0}\033[0;0m'.format(stop - start))

###########################################################3
###########################################################3
###########################################################3

# ##
# ############
# ####Plots 0702
# #######
#Cathode

print('Plots from Idiana University test 07022022')
print('\n')

# print('High Voltage Output Plots')
# plotter(data_dict['HV']['DAC'], data_dict['HV']['Voltage'], 
#         name, xlabel='DAC Code', ylabel='High Voltage Output (|V|)', 
#         x_name='DAC', y_name='HighVoltage', supply='HV')
# print('\n')

print('Cathode large lod')
#Large
name='Cathode_Large_Load_07022022'

plotter(data_0702_LC['HV']['DAC'], data_0702_LC['HV']['Voltage'], 
        name=name, title=name, 
        xlabel='DAC Code', ylabel='DMM Volts', 
        x_name='DAC', y_name='DMM', supply='HV')


plotter(data_0702_LC['C']['DAC'], data_0702_LC['C']['ADC_Voltage'], 
        name='Cathode_Large_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
        x_name='DAC', y_name='ADC_Voltage', supply='Cathode')
plotter(data_0702_LC['C']['DAC'], data_0702_LC['C']['ADC_Current'], 
        name='Cathode_Large_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Current (ADC Code)', 
        x_name='DAC', y_name='ADC_Curent', supply='Cathode')
plotter(data_0702_LC['C']['ADC_Voltage'], data_0702_LC['C']['ADC_Current'], 
        name='Cathode_Large_Load_07022022', title=name, 
        xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
        x_name='ADC_Voltage', y_name='ADC_Current', supply='Same_Cathode')

#different supplies
plotter(data_0702_LC['C']['DAC'], data_0702_LC['P']['ADC_Voltage'], 
        name='Cathode_Large_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
        x_name='DAC', y_name='ADC_Current', supply='Both_Cathode')
plotter(data_0702_LC['C']['DAC'], data_0702_LC['P']['ADC_Current'], 
        name='Cathode_Large_Load_07022022',  title=name, 
        xlabel='DAC Code', ylabel='Current (ADC Code)', 
        x_name='DAC', y_name='ADC_Current', supply='Both_Cathode')

##
#Small
##
print('Cathode small load')

name='Cathode_Small_Load_07022022'

plotter(data_0702_SC['HV']['DAC'], data_0702_SC['HV']['Voltage'], 
        name=name, title=name, 
        xlabel='DAC Code', ylabel='DMM Volts', 
        x_name='DAC', y_name='DMM', supply='HV')


plotter(data_0702_SC['C']['DAC'], data_0702_SC['C']['ADC_Voltage'], 
        name='Cathode_Small_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
        x_name='DAC', y_name='ADC_Voltage', supply='Cathode')
plotter(data_0702_SC['C']['DAC'], data_0702_SC['C']['ADC_Current'], 
        name='Cathode_Small_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Current (ADC Code)', 
        x_name='DAC', y_name='ADC_Curent', supply='Cathode')
plotter(data_0702_SC['C']['ADC_Voltage'], data_0702_SC['C']['ADC_Current'], 
        name='Cathode_Small_Load_07022022', title=name, 
        xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
        x_name='ADC_Voltage', y_name='ADC_Current', supply='Same_Cathode')

#different supplies
plotter(data_0702_SC['C']['DAC'], data_0702_SC['P']['ADC_Voltage'], 
        name='Cathode_Small_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
        x_name='DAC', y_name='ADC_Current', supply='Both_Cathode')
plotter(data_0702_SC['C']['DAC'], data_0702_SC['P']['ADC_Current'], 
        name='Cathode_Small_Load_07022022',  title=name, 
        xlabel='DAC Code', ylabel='Current (ADC Code)', 
        x_name='DAC', y_name='ADC_Current', supply='Both_Cathode')


####
#Potential

print('Plots from Idiana University test 07022022')

print('Potential large lod')
#Large
name='Potential_Large_Load_07022022'


plotter(data_0702_LP['HV']['DAC'], data_0702_LP['HV']['Voltage'], 
        name=name, title=name, 
        xlabel='DAC Code', ylabel='DMM Volts', 
        x_name='DAC', y_name='DMM', supply='HV')



plotter(data_0702_LP['P']['DAC'], data_0702_LP['P']['ADC_Voltage'], 
        name='Potential_Large_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
        x_name='DAC', y_name='ADC_Voltage', supply='Potential')
plotter(data_0702_LP['P']['DAC'], data_0702_LP['P']['ADC_Current'], 
        name='Potential_Large_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Current (ADC Code)', 
        x_name='DAC', y_name='ADC_Curent', supply='Potential')
plotter(data_0702_LP['P']['ADC_Voltage'], data_0702_LP['P']['ADC_Current'], 
        name='Potential_Large_Load_07022022', title=name, 
        xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
        x_name='ADC_Voltage', y_name='ADC_Current', supply='Same_Potential')

#different supplies
plotter(data_0702_LP['P']['DAC'], data_0702_LP['P']['ADC_Voltage'], 
        name='Potential_Large_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
        x_name='DAC', y_name='ADC_Current', supply='Both_Potential')
plotter(data_0702_LP['P']['DAC'], data_0702_LP['P']['ADC_Current'], 
        name='Potential_Large_Load_07022022',  title=name, 
        xlabel='DAC Code', ylabel='Current (ADC Code)', 
        x_name='DAC', y_name='ADC_Current', supply='Both_Potential')

##
#No
##
print('Potential small load')

name='Potential_No_Load_07022022'


plotter(data_0702_NP['HV']['DAC'], data_0702_NP['HV']['Voltage'], 
        name=name, title=name, 
        xlabel='DAC Code', ylabel='DMM Volts', 
        x_name='DAC', y_name='DMM', supply='HV')



plotter(data_0702_NP['P']['DAC'], data_0702_NP['P']['ADC_Voltage'], 
        name='Potential_No_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
        x_name='DAC', y_name='ADC_Voltage', supply='Potential')
plotter(data_0702_NP['P']['DAC'], data_0702_NP['P']['ADC_Current'], 
        name='Potential_No_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Current (ADC Code)', 
        x_name='DAC', y_name='ADC_Curent', supply='Potential')
plotter(data_0702_NP['P']['ADC_Voltage'], data_0702_NP['P']['ADC_Current'], 
        name='Potential_No_Load_07022022', title=name, 
        xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
        x_name='ADC_Voltage', y_name='ADC_Current', supply='Same_Potential')

#different supplies
plotter(data_0702_NP['P']['DAC'], data_0702_NP['C']['ADC_Voltage'], 
        name='Potential_No_Load_07022022', title=name, 
        xlabel='DAC Code', ylabel='Voltage (ADC Code)', 
        x_name='DAC', y_name='ADC_Current', supply='Both_Potential')
plotter(data_0702_NP['P']['DAC'], data_0702_NP['C']['ADC_Current'], 
        name='Potential_No_Load_07022022',  title=name, 
        xlabel='DAC Code', ylabel='Current (ADC Code)', 
        x_name='DAC', y_name='ADC_Current', supply='Both_Potential')


##########################3
####Plots 0722
#######

print('Plots from Idiana University test 07222022')

#Cathode
print('Cathode No lod')
#None
name='Cathode_No_Load_07222022'

plotter(data_0722_C['C']['DAC_Volts'], data_0722_C['C']['ADC_Voltage'], 
        name='Cathode_No_Load_07222022', title=name, 
        xlabel='DAC Volts', ylabel='Voltage (ADC Code)', 
        x_name='DAC_Volts', y_name='ADC_Voltage', supply='Cathode')
plotter(data_0722_C['C']['DAC_Volts'], data_0722_C['C']['ADC_Current'], 
        name='Cathode_No_Load_07222022', title=name, 
        xlabel='DAC Volts', ylabel='Current (ADC Code)', 
        x_name='DAC_Volts', y_name='ADC_Curent', supply='Cathode')
plotter(data_0722_C['C']['ADC_Voltage'], data_0722_C['C']['ADC_Current'], 
        name='Cathode_No_Load_07222022', title=name, 
        xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
        x_name='ADC_Voltage', y_name='ADC_Current', supply='Same_Cathode')

#different supplies
plotter(data_0722_C['C']['DAC_Volts'], data_0722_C['P']['ADC_Voltage'], 
        name='Cathode_No_Load_07222022', title=name, 
        xlabel='DAC Volts', ylabel='Voltage (ADC Code)', 
        x_name='DAC_Volts', y_name='ADC_Current', supply='Both_Cathode')
plotter(data_0722_C['C']['DAC_Volts'], data_0722_C['P']['ADC_Current'], 
        name='Cathode_No_Load_07222022',  title=name, 
        xlabel='DAC Volts', ylabel='Current (ADC Code)', 
        x_name='DAC_Volts', y_name='ADC_Current', supply='Both_Cathode')

###

#Potential
print('Potential No lod')
#None
name='Potential_No_Load_07222022'

plotter(data_0722_P['P']['DAC_Volts'], data_0722_P['P']['ADC_Voltage'], 
        name='Potential_No_Load_07222022', title=name, 
        xlabel='DAC Volts', ylabel='Voltage (ADC Code)', 
        x_name='DAC_Volts', y_name='ADC_Voltage', supply='Potential')
plotter(data_0722_P['P']['DAC_Volts'], data_0722_P['P']['ADC_Current'], 
        name='Potential_No_Load_07222022', title=name, 
        xlabel='DAC Volts', ylabel='Current (ADC Code)', 
        x_name='DAC_Volts', y_name='ADC_Curent', supply='Potential')
plotter(data_0722_P['P']['ADC_Voltage'], data_0722_P['P']['ADC_Current'], 
        name='Potential_No_Load_07222022', title=name, 
        xlabel='Voltage (ADC Code)', ylabel='Current (ADC Code)', 
        x_name='ADC_Voltage', y_name='ADC_Current', supply='Same_Potential')

#different supplies
plotter(data_0722_P['P']['DAC_Volts'], data_0722_P['C']['ADC_Voltage'], 
        name='Potential_No_Load_07222022', title=name, 
        xlabel='DAC Volts', ylabel='Voltage (ADC Code)', 
        x_name='DAC_Volts', y_name='ADC_Current', supply='Both_Potential')
plotter(data_0722_P['P']['DAC_Volts'], data_0722_P['C']['ADC_Current'], 
        name='Potential_No_Load_07222022',  title=name, 
        xlabel='DAC Volts', ylabel='Current (ADC Code)', 
        x_name='DAC_Volts', y_name='ADC_Current', supply='Both_Potential')


############
print('Plots from Chicago University payload test')

##No Load
print('Cathode')

#data_payload = creator_payload(directory+'Chicago_07202022/payload_data.txt')

name = 'Cathode Supply Payload'
payload_plotter(data_payload['VpgmCat'][0:5], data_payload['DMMCat'][0:5], 
        name='Cathode_No_Load_Payload',  title=name, 
        xlabel='Control Volts', ylabel='DMM Volts', 
        x_name='Vpgm_Cathode', y_name='DMM_Cathode', supply='Cathode')



##No Load
print('Potential')

#data_payload = creator_payload(directory+'Chicago_07202022/payload_data.txt')

name = 'Potential Supply Payload'
payload_plotter(data_payload['VpgmPot'][0:5], data_payload['DMMPot'][0:5], 
        name='Potential_No_Load_Payload',  title=name, 
        xlabel='Control Volts', ylabel='DMM Volts', 
        x_name='Vpgm_Potential', y_name='DMM_Potential', supply='Potential')


################################################################
###
'''
1
convert Vpgm cat and pot to DAC code

full_conversion(write_val_d, highvolt_FS, cathode_scale_factor,cathode_volt_FS)

use keith conversions

2
plot IU 0702 data and payload data
make good legend

make for Dac 

3
'''


'''
 newlist = [expression for item in iterable if condition == True] 
'''



def combo_plotter(x, y, x1, y1, data_name, data_name1, title='title', xlabel='x_val', ylabel='y_val', supply='supply', x_name='input', y_name='output'):
    '''
    Simple plot maker. Will make a scatter plot and 
    fit the data with numpy.polyfit()
    '''
    '''
    legend = plt.legend(custom_lines_color, legend_names, loc='best')
    
    custom_lines_style = [Line2D([0], [0], color='k', ls='-'),
                      Line2D([0], [0], color='k', ls='--')]

    '''
    #
    print("Plotting...")
    plt.clf()
    x = np.array(x)
    y = np.array(y)

    theta = np.polyfit(x, y, 1)
    y_line = theta[1] + theta[0] * x
    res = y - y_line
    x_lin = np.linspace(max(x),min(x),1000)
    y_all = theta[1] + theta[0] * x_lin
    
    x1 = np.array(x1)
    y1 = np.array(y1)
    # print(x,y)
    theta1 = np.polyfit(x1, y1, 1)
    # print(theta1[1])
    # print(theta1[0])
    y_line1 = theta1[1] + theta1[0] * x1
    res1 = y1 - y_line1    
    #y_line1 = [0, 1, 1000, 50, 7000]
    x_lin1 = np.linspace(max(x1),min(x1),1000)
    y_all1 = theta1[1] + theta1[0] * x_lin1
    
    
    #vprint(res)
    
    plt.figure(1, figsize = (8,6))
    plt.plot(x_lin,y_all, color='blue', linewidth=1.0)
    plt.scatter(x, y, s=10.0, color='blue', marker="D", label=data_name.replace("_", " "))
    
#    print(y_line1)
    plt.plot(x_lin1,y_all1, color='black', ls='--',linewidth=1.0)
    plt.scatter(x1, y1, s=150.0, color='black', marker="+", label=data_name1.replace("_", " "))

    
    plt.title("{0}".format(title))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5)
    # ax = plt.gca()

    # plt.text(0.1,0.8, "y = {0:5.3f} x + {1:5.3f}".format(theta[0],theta[1]),
    #          transform = ax.transAxes, size=10, color="red")
    

    # custom_legend = [Line2D([0], [0], color='blue'),
    #                  Line2D([0], [0], color='black')]

    # legend = plt.legend(custom_legend, [data_name, data_name1], loc='best')
    plt.legend()


    plt.savefig("test_plots/{0}_{1}_{2}_{3}_{4}.png".format(data_name,data_name1,supply,x_name,y_name),dpi=300)
    plt.clf()
    
    
    print('Done!')
    return theta, theta1



def baby_plotter(x, y, data_name, title='title', xlabel='x_val', ylabel='y_val',
                 fit_color='red', color='blue', marker='D',
                 supply='supply', x_name='input', y_name='output', clear = False):
    '''
    '''
    #
    print("Plotting...")
    
    x = np.array(x)
    y = np.array(y)
    
    theta = np.polyfit(x, y, 1)
    y_line = theta[1] + theta[0] * x
    res = y - y_line

    x_lin = np.linspace(max(x),min(x),1000)
    y_all = theta[1] + theta[0] * x_lin
    
    label = data_name.replace("_"," ")
    
    plt.figure(1, figsize = (8,6))
    plt.plot(x_lin,y_all, color=fit_color, linewidth=1.0)
    plt.scatter(x, y, s=10.0, color=color, marker=marker, label=label)
    
    
    plt.title("{0}".format(title))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5)
    # ax = plt.gca()

    # plt.text(0.1,0.8, "y = {0:5.3f} x + {1:5.3f}".format(theta[0],theta[1]),
    #          transform = ax.transAxes, size=10, color="red")
    
    # custom_legend = [Line2D([0], [0], color='blue'),
    #                  Line2D([0], [0], color='black')]

    # legend = plt.legend(custom_legend, [data_name, data_name1], loc='best')
    
    plt.legend()

    
    if clear == True:
        plt.savefig("test_plots/{0}_{1}_{2}_{3}_{4}.png".format(data_name,supply,x_name,y_name),dpi=300)
        plt.clf()
    else:
        print('Done!')
    
    return



'''
plotter(data_0702_LP['HV']['DAC'], data_0702_LP['HV']['Voltage'], 
        name=name, title=name, 
        xlabel='DAC Code', ylabel='DMM Volts', 
        x_name='DAC', y_name='DMM', supply='HV')

def combo_plotter(x, y, x1, y2, data_name, data_name1, title='title', xlabel='x_val', ylabel='y_val', supply='supply', x_name='input', y_name='output'):

'''


#For IU 0702 and Payload test


#ADC
# combo_plotter(data_0702_LC['HV']['DAC'], data_0702_LC['HV']['Voltage'], Cat_control, data_payload['DMMCat'][0:5],
#               data_name='IU_0702_Large_Load', data_name1='UC_Payload_No_Load', title=name, 
#               xlabel='DAC Code', ylabel='DMM Volts', 
#               x_name='DAC', y_name='ADC_Voltage', supply='Cathode')


# name = 'Potential Supply'
# combo_plotter(data_0702_NP['HV']['DAC'], data_0702_NP['HV']['Voltage'], Cat_control, data_payload['DMMPot'][0:5],
#               data_name='IU_0702_Large_Load', data_name1='UC_Payload_No_Load', title=name, 
#               xlabel='DAC Code', ylabel='DMM Volts', 
#               x_name='DAC', y_name='DMM', supply='Potential')


# def baby_plotter(x, y, data_name, title='title', xlabel='x_val', ylabel='y_val',
#                  fit_color='red', color='blue', marker='D',
#                  supply='supply', x_name='input', y_name='output', clear = False):

#Cat_control, data_payload['DMMCat'][0:5]
# baby_plotter(data_0702_LC['HV']['DAC'], data_0702_LC['HV']['Voltage'],
#               data_name='IU_0702_Large_Load', title=name, 
#               xlabel='DAC Code', ylabel='DMM Volts', 
#               x_name='DAC', y_name='DMM', supply='Cathode', clear=False)


def triple_plotter(x, y, x1, y1, x2, y2, data_name, data_name1, data_name2, 
                   title='title', xlabel='x_val', ylabel='y_val', 
                   supply='supply', x_name='input', y_name='output'):
    '''
    Simple plot maker. Will make a scatter plot and 
    fit the data with numpy.polyfit()
    '''
    '''
    legend = plt.legend(custom_lines_color, legend_names, loc='best')
    
    custom_lines_style = [Line2D([0], [0], color='k', ls='-'),
                      Line2D([0], [0], color='k', ls='--')]

    '''
    print("Plotting...")

    #fit and data
    x = np.array(x)
    y = np.array(y)
    theta = np.polyfit(x, y, 1)
    y_line = theta[1] + theta[0] * x
    res = y - y_line
    x_lin = np.linspace(max(x),min(x),1000)
    y_all = theta[1] + theta[0] * x_lin
    
    x1 = np.array(x1)
    y1 = np.array(y1)
    theta1 = np.polyfit(x1, y1, 1)
    y_line1 = theta1[1] + theta1[0] * x1
    res1 = y1 - y_line1    
    x_lin1 = np.linspace(max(x1),min(x1),1000)
    y_all1 = theta1[1] + theta1[0] * x_lin1
   
    x2 = np.array(x2)
    y2 = np.array(y2)
    theta2 = np.polyfit(x2, y2, 1)
    y_line2 = theta2[1] + theta2[0] * x2
    res2 = y2 - y_line2    
    x_lin2 = np.linspace(max(x2),min(x2),1000)
    y_all2 = theta2[1] + theta2[0] * x_lin2
   
    #plot
    plt.figure(1, figsize = (8,6))

    plt.plot(x_lin,y_all, color='blue', linewidth=1.0)
    plt.scatter(x, y, s=10.0, color='blue', marker="D", label=data_name.replace("_", " "))
    
    plt.plot(x_lin1,y_all1, color='black', ls='--',linewidth=1.0)
    plt.scatter(x1, y1, s=150.0, color='black', marker="+", label=data_name1.replace("_", " "))

    plt.plot(x_lin2,y_all2, color='red', ls='-.',linewidth=1.0)
    plt.scatter(x2, y2, s=30.0, color='red', marker="*", label=data_name2.replace("_", " "))

    plt.title("{0}".format(title))
    plt.xlabel(xlabel, labelpad = 0.5, fontsize = 10)
    plt.ylabel(ylabel, labelpad = 0.5, fontsize = 10)
    plt.grid(visible=True, which='both', axis='both', linestyle='--', linewidth=0.5)
    # ax = plt.gca()

    # plt.text(0.1,0.8, "y = {0:5.3f} x + {1:5.3f}".format(theta[0],theta[1]),
    #          transform = ax.transAxes, size=10, color="red")
    

    # custom_legend = [Line2D([0], [0], color='blue'),
    #                  Line2D([0], [0], color='black')]

    # legend = plt.legend(custom_legend, [data_name, data_name1], loc='best')
    plt.legend()


    plt.savefig("test_plots/{0}_{1}_{2}_{3}_{4}_{5}.png".format(supply,data_name,data_name1,data_name2,
                                                                x_name,y_name),dpi=300)
    plt.clf()
    
    
    print('Done!')
    return theta, theta1, theta2


#####
##Plots
####

Cat_Control = [full_conversion(x, highvolt_FS, cathode_scale_factor,cathode_volt_FS) for x in data_payload['VpgmCat'][0:5]]

Pot_Control = [full_conversion(x, highvolt_FS, potential_voltage_scale_factor,potential_volt_FS) for x in data_payload['VpgmPot'][0:5]]

Cat_ADC = [x/conv_factor_HV for x in data_payload['VmonCat'][0:5]]
Pot_ADC = [x/conv_factor_HV for x in data_payload['VmonPot'][0:5]]


#########3
name = 'Cathode Supply'

print("Cathode Plots")
#IU 0702 & Paylaod
#DMM
theta, theta1 = combo_plotter(data_0702_LC['HV']['DAC'], data_0702_LC['HV']['Voltage'], Cat_Control, data_payload['DMMCat'][0:5],
              data_name='IU_0702_36_MOhm_Load', data_name1='UC_Payload_No_Load', title=name, 
              xlabel='DAC Code', ylabel='DMM Volts', 
              x_name='DAC', y_name='DMM', supply='Cathode')

print("This is for IU 0702 & Payload")
print("IU 0702")
print(theta)
print("UC Payload")
print(theta1)

#ADC 
combo_plotter(data_0702_LC['C']['DAC'], data_0702_LC['C']['ADC_Voltage'], Cat_Control, Cat_ADC,
              data_name='IU_0702_36_MOhm_Load', data_name1='UC_Payload_No_Load', title=name, 
              xlabel='DAC Code', ylabel='ADC Vmon Code', 
              x_name='DAC', y_name='ADC_Voltage', supply='Cathode')

#IU 0702 & 0722 & Payload
#ADC 
theta, theta1, theta2 = triple_plotter(data_0702_LC['C']['DAC'], data_0702_LC['C']['ADC_Voltage'], 
               Cat_Control, Cat_ADC, data_0722_C['C']['DAC_Volts'], data_0722_C['C']['ADC_Voltage'], 
               data_name='IU_0702_36_MOhm_Load', data_name1='UC_Payload_No_Load', data_name2='IU_0722_No_Load', 
               title=name, xlabel='DAC Code', ylabel='ADC Vmon Code', 
               x_name='DAC', y_name='ADC_Voltage', supply='Cathode')

print("This is for ADC Vmon Code")
print("IU 0702")
print(theta)
print("UC Payload")
print(theta1)
print("IU 0722")
print(theta2)
##############3

#########3
name = 'Potential Supply'

print("Potential Plots")
#IU 0702 & Paylaod
#DMM
DMM_theta, DMM_theta1 = combo_plotter(data_0702_NP['HV']['DAC'], data_0702_NP['HV']['Voltage'], 
                              Pot_Control, data_payload['DMMPot'][0:5], data_name='IU_0702_No_Load', 
                              data_name1='UC_Payload_No_Load', title=name, 
                              xlabel='DAC Code', ylabel='DMM Volts', 
                              x_name='DAC', y_name='DMM', supply='Potential')

print("This is for IU 0702 & Payload")
print("IU 0702")
print(DMM_theta)
print("UC Payload")
print(DMM_theta1)

#ADC 
combo_plotter(data_0702_NP['P']['DAC'], data_0702_NP['P']['ADC_Voltage'], Pot_Control, Pot_ADC,
              data_name='IU_0702_No_Load', data_name1='UC_Payload_No_Load', title=name, 
              xlabel='DAC Code', ylabel='ADC Vmon Code', 
              x_name='DAC', y_name='ADC_Voltage', supply='Potential')

#IU 0702 & 0722 & Payload
#ADC 
ADC_theta, ADC_theta1, ADC_theta2 = triple_plotter(data_0702_NP['P']['DAC'], data_0702_NP['P']['ADC_Voltage'], 
               Pot_Control, Pot_ADC, data_0722_P['P']['DAC_Volts'], data_0722_P['P']['ADC_Voltage'], 
               data_name='IU_0702_No_Load', data_name1='UC_Payload_No_Load', data_name2='IU_0722_No_Load', 
               title=name, xlabel='DAC Code', ylabel='ADC Vmon Code', 
               x_name='DAC', y_name='ADC_Voltage', supply='Potential')

print("This is for ADC Vmon Code")
print("IU 0702")
print(ADC_theta)
print("UC Payload")
print(ADC_theta1)
print("IU 0722")
print(ADC_theta2)
##############3

'''
Next need to find function from fitted parameters to go from DMM to ADC and ADC to DMM
the 'theta' array above has index 0 for slope and index 1 for the offset

the below should work for whatver supply you put in
'''
def ADC_to_DMM(DMM_theta, ADC_theta, ADC):
    '''
    You put in an ADC value.
    You get out a DMM value
    '''
    DMM = (DMM_theta[0]/ADC_theta[0]) * (ADC - ADC_theta]1]) + DMM_theta[1] 
    return DMM

def DMM_to_ADC(ADC_theta, DMM_theta, DMM):
    '''
    You put in a DMM value.
    You get out an ADC value.
    '''
    ADC = (ADC_theta[0]/DMM_theta[0]) * (DMM - DMM_theta[1] ) + ADC_theta[1] 
    return ADC



# def payload_plotter(x, y, name, title='title', xlabel='x_val', ylabel='y_val', supply='HV', x_name='input', y_name='data'):
#     '''
#     Simple plot maker. Will make a scatter plot and 
#     fit the data with numpy.polyfit()
#     '''


# payload_plotter(     





##End of script##
stop = timeit.default_timer()
print('Time: \033[1;31m{0}\033[0;0m'.format(stop - start))
exit()




