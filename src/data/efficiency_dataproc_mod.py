# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 09:40:20 2021

Efficiency pilot structural 2p processing module.
'fr' is short for frames.


@author: dpaynter
"""

import numpy as np
import tifffile as tf
from PIL import Image

def frame_sep_avg(tiff_file_path, save_path, fr_per_plane, num_chan):
    """Takes a multi-page tiff file acquired at BScope2, the number of frames
    taken at the same z location, the mouse name, and the "stackID" or an identifyer
    for the imaging region.
    Returns one tif for each z plane in the stack."""
    
    file = tf.imread(tiff_file_path) 
    num_fr = file.shape[0]
    
    if num_chan == 2:
        chan1 = file[::2,:,:]
        chan2 = file[1::2,:,:]
        chans = [chan1, chan2]
    else:
        chans = file
    num_outputs = int(np.floor((num_fr / fr_per_plane))) - 1
    
    for zplane in range(num_outputs):
        startframe = int(zplane*fr_per_plane)
       
        for it, channel in enumerate(chans):
            if zplane == num_outputs:
                output_z = np.average(channel[[startframe,num_fr-1],:,:], axis=0)
            else:
          
                output_z = np.sum(channel[[startframe + it,(startframe+it+fr_per_plane)],:,:], axis=0)
            tf.imsave(save_path + str(zplane) + '_' + str(it) + '.tif', output_z)
            img = Image.fromarray(np.uint8(output_z * (255/(np.max(output_z)))) , 'L')
            img.save(save_path + str(zplane) + '_' + str(it) + '.png')
                
