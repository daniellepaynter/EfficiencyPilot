#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Script to support processing imagedata using suite2p.

Created on Tue Apr 29, 2020

@author: pgoltstein
"""

from os import path
import numpy as np
from suite2p import run_s2p
from suite2p.registration import register
from PIL import Image, ImageSequence

def set_dataonsetframe(dataonsetframe, datapath="."):
    """ Sets the data onset frame by excluding the frames before data onset using the badframes approach
    """
    bad_frames = np.arange(0,dataonsetframe,1,dtype=np.int)
    np.save(path.join(datapath,'bad_frames.npy'), bad_frames)

def generate_ops( datapath, sf, tau=1.5, nplanes=1, nchannels=1, functional_chan=1, align_by_chan=1, aspect=1.0, neuron_size_px_yx=[10,10], fast_disk=[], batch_size=500, include_frames=-1, two_step_registration=False, do_nonrigid=False ):

    ops = run_s2p.default_ops()

    # file paths
    ops['look_one_level_down'] = False
    ops['fast_disk'] = fast_disk
    ops['delete_bin'] = False
    ops['save_path0'] = datapath
    ops['save_folder'] = "suite2p"
    ops['subfolders'] = []
    ops['data_path'] = [datapath,]

    # main settings
    ops['nplanes'] = nplanes # each tiff has these many planes in sequence
    ops['nchannels'] = nchannels # each tiff has these many channels per plane
    ops['functional_chan'] = functional_chan # functional channel (1-based)
    ops['tau'] = tau # Deconv. GCaMP6f: 0.7; GCaMP6m: 1.0; GCaMP6s: 1.25-1.50
    ops['fs'] = sf  # sampling rate per plane
    ops['frames_include'] = include_frames

    # output settings
    ops['preclassify']= 0.0 # classifier bef signal extraction e.g. prob=0.3
    ops['save_mat'] = False # whether to save output as matlab files
    ops['combined'] = False # combine multiple planes into a single result
    ops['aspect']: aspect # um/pixels in X / um/pixels in Y (for GUI)

    # bidirectional phase offset
    ops['do_bidiphase'] = True
    ops['bidiphase'] = 0
    ops['bidi_corrected'] = False

    # registration settings
    ops['do_registration'] = 1 # 1=register data once; 2 forces re-registration
    ops['two_step_registration'] = two_step_registration
    ops['keep_movie_raw'] = False
    ops['nimg_init'] = 300 # subsampled frames for finding reference image
    ops['batch_size'] = batch_size # number of frames per batch
    ops['maxregshift'] = 0.1 # max allowed registr shift in fraction of image
    ops['align_by_chan'] = align_by_chan # align by this channel (1-based)
    ops['reg_tif'] = False # whether to save registered tiffs
    ops['reg_tif_chan2'] = False # whether to save channel 2 registered tiffs
    ops['subpixel'] = 10 # precision of subpixel registration (1/subpixel steps)
    ops['smooth_sigma_time'] = 0 # gaussian smoothing in time
    ops['smooth_sigma'] = 1.15 # ~1 for 2P recordings, >5 for 1P recordings
    ops['th_badframes'] = 1.0 # set it <1.0 to exclude more frames
    ops['pad_fft'] = False

    # non rigid registration settings
    ops['nonrigid'] = do_nonrigid # whether to use nonrigid registration
    ops['block_size'] = [128, 128] # keep this a multiple of 2
    ops['snr_thresh'] = 1.2 # if any nonrigid block is below this threshold, it gets smoothed until above this threshold. 1.0 results in no smoothing
    ops['maxregshiftNR'] = 10 # maximum pixel shift allowed for nonrigid, relative to rigid

    # cell detection settings
    ops['roidetect'] = True # whether or not to run ROI extraction
    ops['sparse_mode'] = False # whether or not to run sparse_mode
    ops['diameter'] = neuron_size_px_yx # diameter for filtering and extracting
    ops['spatial_scale'] = 0 # 0: multi-scale; 1: 6 pixels, 2: 12 pixels, etc
    ops['connected'] = True # keep ROIs fully connected? (set 0 for dendrites)
    ops['nbinned'] = 5000 # max number of binned frames for cell detection
    ops['max_iterations'] = 20 # max num of iterations to do cell detection
    ops['threshold_scaling'] = 1.0 # adjust the automatically determined threshold by this scalar multiplier
    ops['max_overlap'] = 0.75 # remove cells with more overlap than this
    ops['high_pass'] = 100 # running mean subtraction with window of size 'high_pass' (use low values for 1P)

    # ROI extraction parameters
    ops['inner_neuropil_radius'] = 2
    ops['min_neuropil_pixels'] = 350
    ops['allow_overlap'] = False

    # channel 2 detection settings (stat[n]['chan2'], stat[n]['not_chan2'])
    ops['chan2_thres'] = 0.65 # minimum for detection of brightness on chan 2

    # deconvolution settings
    ops['baseline'] = 'maximin' # baselining mode (can also choose 'prctile')
    ops['win_baseline'] = 60.0 # window for maximin
    ops['sig_baseline'] = 10.0 # smoothing constant for gaussian filter
    ops['prctile_baseline'] = 8.0 # optional
    ops['neucoeff'] = 0.7 # neuropil coefficient

    return ops
