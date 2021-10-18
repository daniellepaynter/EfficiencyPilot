# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 11:03:11 2021

Script to create the sub-directories for efficiency pilot processed 2P data,
in the I/archive drive.

@author: dpaynter
"""

### Set the variables: 
mouse = 'DP_210520'
experiment_date = '210830'
num_locs = 3

### Imports:
import os

locs = ['loc1', 'loc2', 'loc3', 'loc4', 'loc5', 'loc6', 'loc7', 'loc8', 'loc9', 'loc10']

date_folder = os.path.join(r"I:/Danielle Paynter/InVivoTTTPilots/efficiency_pilot/data/processed", mouse, "2P", experiment_date)

os.makedirs(date_folder)
for loc in range(num_locs):
    os.makedirs(os.path.join(date_folder, locs[loc], "1_avg_MATLAB", "Ch1"))
    os.makedirs(os.path.join(date_folder, locs[loc], "1_avg_MATLAB", "Ch2"))
    os.makedirs(os.path.join(date_folder, locs[loc], "2_smooth_contrast_FIJI", "Ch1"))
    os.makedirs(os.path.join(date_folder, locs[loc], "2_smooth_contrast_FIJI", "Ch2"))
    os.makedirs(os.path.join(date_folder, locs[loc], "3_etc"))

##########################################################################

