# #!/bin/bash 

# ######################################
# #             HELIX                  #
# #   Plot Maker High Voltage Test     #
# #        Dennis H. Calderon          #
# #    calderon-madera.1@osu.edu       #
# ######################################

# #######################################################
# """
# =======================
# ##Plot_Maker_High_Voltage_Test.sh##
# ======================
# Author: Dennis H. Calderon
# Email: calderon-madera.1@osu.edu
# Date: July 05, 2022
# Modified: 
# =======================
# Descripiton: 
# This SHELL script will run the PYTHON script 
# High_Voltage_Test_Plot.py for the given raw data files 
# rom the High Voltage test done at Indiana University 
# July 02, 2022. 

# I don't want to continue running the sript individually 
# every time. 

# Maybe I can also write a new script or add to this to also 
# prep the files for use in the PYTHON script. 

# The test was done for both supply 1 (under load) and 
# supply 2 (under load and no load). Data was taken by hand 
# (Me) for given DAC and voltage reading. Data was saved from 
# serial output of DAC and ADC_Voltage and ADC_Current for 
# POTENTIAL supply and CATHODE supply.

# The script will create plots for DAC vs other variables when it can and 
# also fit a line and label the paramers when appropiate.

# Note:
# The files should be prepped using,
#  grep | sed > filename.txt
# =======================
# Usage:
# bash Plot_Makder_High_Voltage_Test.sh

# =======================
# Options:

# =======================
# example:

# =======================
# """
#######################################################

python High_Voltage_Test_Plot.py raw_data/Supply_1_Load_26M_Ohm.csv raw_data/small_load_HVsupply1_07022022_raw_clean.txt

python High_Voltage_Test_Plot.py raw_data/Supply_1_Load_36M_Ohm.csv raw_data/large_load_HVsupply1_07022022_raw_clean.txt

python High_Voltage_Test_Plot.py raw_data/Supply_2_Load_36M_Ohm.csv raw_data/large_load_HVsupply2_07022022_raw_clean.txt

python High_Voltage_Test_Plot.py raw_data/Supply_2_Load_None.csv raw_data/no_load_HVsupply2_07022022_raw_clean.txt

mv test_plots/*Masked*png test_plots/masked/. 
