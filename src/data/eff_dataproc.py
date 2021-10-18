# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 10:39:09 2021

@author: dpaynter
"""
###################
#Imports:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2
import sys
import eff_landmark_picker as elp
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import os
import os.path


###################
#Step 0: Input key information:
    
mouse_name = input("Which mouse will you process data from?")
loc_ID = input("Which location are you processing data from?")
num_dates = int(input("How many imaging dates are you processing for this mouse/location?"))
date0 = input("Path to first timepoint:")
date1 = input("Path to second timepoint:")
date2 = input("Path to third timepoint:")

dates = []
dates.append(date0)
dates.append(date1)
dates.append(date2)
###################
#Step 1: Preprocess data in other softwares:
    
input("Check mouse {}, {}, in {} dates for 1_avg_MATLAB files, then press enter.".format(mouse_name, loc_ID, num_dates))
input("Check for 5_n2v_RGB files, then press enter.")

###################
#Step 2: use eff_landmark_picker to get points that will be used to align images:
    
check_csv = input("If a landmarks excel file already exists, input the full path and file name; if not, type 'no'.")
if check_csv == "no": 
    input(elp.elp((mouse_name + '_' + loc_ID), num_dates))
    path_to_landmarks_csv = input("Copy/paste the path to landmarks file:")

else:
    try:
        path_to_landmarks_csv = check_csv
    except:
        print("Invalid path to landmarks excel file.")
        quit()

###################
#Step 3: Organize the exported spreadsheet, so that points can be used to align image frames:
    
df = pd.read_excel(path_to_landmarks_csv)
df.insert(5, "set", "empty")

grouped_imnum = df.groupby(df.im_num)
index_count = 0

for name, group in grouped_imnum:
    im_group = grouped_imnum.get_group(name)
    grouped_zval = im_group.groupby("z")
    zval_count = 0
    for name, group in grouped_zval:
        zval_group = grouped_zval.get_group(name)
        zval = list(zval_group["z"])[0]
        df["set"] = np.where(df["z"]==zval, zval_count, df["set"])
        zval_count+=1
        index_count+=1


###################
#Step 4: For each set of z-planes, match one to the other:


grouped_set = df.groupby(df.set)
warped_ims = []
for name, group in grouped_set:
    set_df = grouped_set.get_group(name)
    subgrouped = set_df.groupby("im_num")
    
    x_points = []
    y_points = []
    
    im_list = []
    
    date = 0
    for name, group in subgrouped:
        subgroup = subgrouped.get_group(name)
        x_points.append(subgroup.x)
        y_points.append(subgroup.y)
        
        
        im_pts_list = []
        for it, pt in enumerate(x_points):
            im_pts_list.append(pd.concat((x_points[it], y_points[it]), axis=1))
        im_pts = [data.to_numpy(dtype='float32') for data in im_pts_list]
        
        im_path = os.path.join(dates[date], loc_ID, '5_n2v_RGB', ('Plane00' + str(list(subgroup.z)[0]+1) + '.tif'))
        im_list.append(cv2.imread(im_path))
        date+=1

    points1 = im_pts[0]
    points2 = im_pts[1]
    
    h, mask = cv2. findHomography(points1, points2)
    im1 = im_list[0]
    im2 = im_list[1]
    
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))
    warped_ims.append(im1Reg)
    
###################

    
    
