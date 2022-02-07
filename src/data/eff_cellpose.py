# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 13:59:53 2021

Cellpose initial try

@author: dpaynter
"""

import numpy as np
import time, os, sys
import os.path
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300
from cellpose import utils, io

from cellpose import models, io
model = models.Cellpose(gpu=True, model_type='cyto')
chan = [0, 0]

files = []
path_to_ims = r'I:\Danielle Paynter\InVivoTTTPilots\efficiency_pilot\data\processed\DP_210519A\210617\loc5\test_data'

for root, dirs, ts in os.walk(path_to_ims):
	for file in ts:
        #append the file name to the list
		files.append(os.path.join(root,file))
        
for filename in files:
    img = io.imread(filename)
    masks, flows, styles, diams = model.eval(img, diameter=23, channels=chan)
    
    io.masks_flows_to_seg(img, masks, flows, diams, filename, chan)
    
    io.save_to_png(img, masks, flows, filename)