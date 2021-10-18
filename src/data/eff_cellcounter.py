# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 14:10:36 2021

@author: dpaynter
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
import sys
import os.path
import importlif as il

im_folder = r'I:\Danielle Paynter\InVivoTTTPilots\efficiency_pilot\data\processed\DP_210429\2P\210602\loc1\6_z'
ims = os.listdir(im_folder)
im_list = []
for it, im in enumerate(ims):
    im_path = os.path.join(im_folder, im)
    im_list.append(cv2.imread(im_path, cv2.IMREAD_GRAYSCALE))
    
im_stack = np.asarray(im_list)
im_stack = np.moveaxis(im_stack, 0, 2)

blobs = il.cellcount(im_stack)
circd = il.circleblobs(blobs, im_stack)

cell_count = sum([blobs[arr].shape[0] for arr in range(len(blobs))])