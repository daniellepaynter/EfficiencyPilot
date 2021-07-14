# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 12:04:21 2021

Efficiency pilot structural 2p processing script.
Uses function "frame_sep_avg" from the efficiency_dataproc_mod module.
Produces a tif and png for each z-plane in each multi-tif file in a given folder; for example,
for all imaging positions on a given da.



@author: dpaynter
"""

tiff_folder_path = r'I:\Danielle Paynter\InVivoTTTPilots\efficiency_spread_pilot\data\raw\DP_210429\2P'
save_folder_path = r'I:\Danielle Paynter\InVivoTTTPilots\efficiency_spread_pilot\data\processed\DP_210429\2P\210524\\'


import efficiency_dataproc_mod as eff  
from os import listdir

stack_names = list()

for file in listdir(tiff_folder_path):
    if file.endswith(".tif"):
        stack_names.append(file)

for stack in stack_names:
    shortstack = stack.replace('.tif', '_')
    save_path = save_folder_path + shortstack
    try:
        eff.frame_sep_avg(tiff_folder_path + '\\' + stack, save_path, 150, 1)
    except:
        pass