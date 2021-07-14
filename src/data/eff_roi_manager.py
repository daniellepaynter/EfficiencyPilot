# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 16:55:29 2021

Reads in ROI zip file exported from JB's FIJI plug-in "ROI Group Manager"

@author: dpaynter
"""
import numpy as np
from read_roi import read_roi_zip as rrz

rois = rrz(r'I:\Danielle Paynter\InVivoTTTPilots\efficiency_spread_pilot\data\interim\loc1_hyperstacks\RoiSet.zip')


all_roi_IDs = []

for roi in rois:
    roinames = rois[roi]['name'].split()
    roiname = roinames[0]
    all_roi_IDs.append(int(roiname))
    
roi_IDs = list(set(all_roi_IDs))
roi_IDs.sort()

roi_array = np.zeros([len(roi_IDs), 6])
roi_array[:,0] = roi_IDs

for roi in rois:
    roinames = rois[roi]['name'].split()
    roiname = int(roinames[0])
    all_roi_IDs.append(roiname)
    im_nr = int(roinames[1])
    roi_array[roiname-1, im_nr] = 255



output_table = np.zeros([37,5])


print(rois[roi]['position']['frame'])