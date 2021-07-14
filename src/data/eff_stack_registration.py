# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 16:23:22 2021

Registers stacks from different timepoints.

@author: dpaynter
"""
## INPUTS:
    
tiff_file_path = r'I:\Danielle Paynter\InVivoTTTPilots\efficiency_spread_pilot\data\processed\DP_210429\2P\stacks_by_loc_date'

###################################

import numpy as np
import pystackreg as psr
import tifffile as tf
from PIL import Image

files = tf.imread(tiff_file_path) 