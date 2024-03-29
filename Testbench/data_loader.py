#System libraries
import csv

#Python libraries
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import matplotlib.style as style

#Other
from test_hv_conversions import *
##########################################


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



#########3
#Plotting functions
###########

        
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
    
    return

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
    return
####33




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

