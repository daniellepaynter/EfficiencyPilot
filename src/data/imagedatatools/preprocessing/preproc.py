#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Functions to run image and roi processing of calcium imaging data (using suite2p)

Created on Mon Apr 27, 2020

@author: pgoltstein
"""

import sys, os, glob, time
import numpy as np
from suite2p import run_s2p
from suite2p.io import tiff
from suite2p.registration import register
from suite2p.extraction import extract, dcnv

# Detect operating system and add local import dir
if "darwin" in sys.platform.lower(): # MAC OS X
    sys.path.append('/Users/pgoltstein/code/python/auxdata')
    sys.path.append('/Users/pgoltstein/code/python/imagestack')
    sys.path.append('/Users/pgoltstein/code/python/imagedatatools')
elif "win" in sys.platform.lower(): # Windows
    sys.path.append('D:/code/auxdata')
    sys.path.append('D:/code/imagestack')
    sys.path.append('D:/code/imagedatatools')

# Local imports
import auxrecorder
import scanimagestack
import suite2pdata


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Functions

def calculate_lightleak_pixels(Im, Aux, threshold):
    """ Determines the pixels on the sides of the image that are affected by the monitor light leak. Produces an image from the darkframes, and calculates applies a threshold set in the processing settings.
    """

    # Get darkframes
    darkframe_onset, darkframe_offset = Aux.darkframes

    # Get the mean over the x-dimension
    Im_df = np.mean(Im[darkframe_onset:darkframe_offset], axis=2)

    # Find pixels on left and right that are brighter than threshold
    lightleak = (np.mean(Im_df,axis=0) > threshold) * 1.0

    # Set to 0 if the first pixel is below threshold, otherwise find pixel
    if lightleak[0] == 0:
        px_left = 0.0
    else:
        px_left = np.argwhere( np.diff(lightleak) == -1.0 )[0]
    if lightleak[-1] == 0:
        px_right = Im_df.shape[1]-1
    else:
        px_right = np.argwhere( np.diff(lightleak) == 1.0 )[-1]

    # Return left,right as integer
    return int(px_left), int(px_right)


def run_preprocessing( datapath=None, settingspath=None ):
    """ This function loads the settings files (if present) and starts the processing of the image stack using suite2p
    """

    # Find settings
    if settingspath is not None:

        # Find image settings
        imagesettingsfile = glob.glob( os.path.join( settingspath, "*.imagesettings.py" ) )[0]
        if not imagesettingsfile:
            imagesettingsfile = None

        # Find aux settings
        auxsettingsfile = glob.glob( os.path.join( settingspath, "*.auxsettings.py" ) )[0]
        if not auxsettingsfile:
            auxsettingsfile = None

        # Find preprocessing settings
        preprocsettingsfile = glob.glob( os.path.join( settingspath, "*.preprocsettings.py" ) )[0]
        if not preprocsettingsfile:
            preprocsettingsfile = None
    else:
        imagesettingsfile = None
        auxsettingsfile = None
        preprocsettingsfile = None

    # Set preprocessing settings file to default (if none supplied)
    if preprocsettingsfile is None:
        self_path = os.path.dirname(os.path.realpath(__file__))
        settings_path = os.path.join( os.path.sep.join(  self_path.split(os.path.sep)[:-1] ), "settings" )
        preprocsettingsfile = os.path.join(settings_path,"default.preprocsettings.py")

    # Load preprocessing settings
    preprocsettings = {}
    with open(preprocsettingsfile) as f:
        exec(f.read(), preprocsettings)
        preprocsettings = preprocsettings["preprocsettings"]

    # Add the paths and settings files
    preprocsettings["datapath"] = datapath
    preprocsettings["settingspath"] = settingspath
    preprocsettings["imagesettingsfile"] = imagesettingsfile
    preprocsettings["auxsettingsfile"] = auxsettingsfile
    preprocsettings["preprocsettingsfile"] = preprocsettingsfile


    #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

    # Start
    print("\nPreprocessing {}".format(datapath))
    print("* Preprocessing settings: {}\n".format(preprocsettingsfile))
    t0 = time.time()

    # Open imagestack
    Im = scanimagestack.XYT(filepath=datapath, imagesettingsfile=imagesettingsfile)
    print("{}\n".format(Im))

    # Load aux data
    Aux = auxrecorder.LvdAuxRecorder( filepath=datapath, auxsettingsfile=auxsettingsfile, nimagingplanes=Im.nplanes )
    print("{}\n".format(Aux))

    # Calculate derived parameters
    aspect_ratio = Im.fovsize["x"]/Im.fovsize["y"]
    print("Aspect ratio = {} X/Y".format(aspect_ratio))
    neuron_size_px_yx = [ int(np.round(preprocsettings["neuron_size_micron"] / Im.pixelsize["y"])), int(np.round(preprocsettings["neuron_size_micron"] / Im.pixelsize["x"])) ]
    print("Neuron size is set to {} by {} pixels yx".format(neuron_size_px_yx[0],neuron_size_px_yx[1]))

    # Exclude monitor light at image sides using cropping-settings
    if preprocsettings["lightleak_threshold"] is not None:
        print("Detecting possible monitor light-leak.")
        print("Darkframes: {}--{},  threshold: {}".format( Aux.darkframes[0], Aux.darkframes[1], preprocsettings["lightleak_threshold"]))
        px_left, px_right = calculate_lightleak_pixels(Im, Aux, preprocsettings["lightleak_threshold"])
        preprocsettings["im_xrange"] = np.array([px_left, px_right])
        print("Adjusted imaging x-range: {}--{} px\n".format(px_left, px_right))
    else:
        print("Skipping detection of possible monitor light-leak, using full image\n")
        preprocsettings["im_xrange"] = np.array([0, Im.xres])

    # Include only frames after data onset frame by setting badframes
    print("Setting frame {} as data onset frame\n".format(Aux.dataonsetframe))
    suite2pdata.set_dataonsetframe(Aux.dataonsetframe, datapath=datapath)

    # Create suite2p options & settings
    general_options = suite2pdata.generate_ops( datapath, Aux.imagingsf, tau=preprocsettings["tau"], nplanes=Im.nplanes, nchannels=Im.nchannels, functional_chan=preprocsettings["functional_channel"], align_by_chan=preprocsettings["align_by_channel"], aspect=aspect_ratio, neuron_size_px_yx=neuron_size_px_yx, fast_disk=preprocsettings["fast_disk"], batch_size=500, do_nonrigid=preprocsettings["do_nonrigid"])
    general_options_save_file = os.path.join(general_options['save_path0'], general_options['save_folder'], 'ops1.npy')
    preprocsettings_save_file = os.path.join(general_options['save_path0'], general_options['save_folder'], 'preprocsettings.npy')

    #<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
    # Run suite2p semi-manual
    print("Starting suite2p routines")

    # Read tiffs, convert to binaries
    options_per_plane = tiff.tiff_to_binary(general_options)
    np.save(general_options_save_file, options_per_plane)
    print("Wrote tifs to binaries for {} planes ({:0.1f} s)".format( len(options_per_plane), time.time()-t0 ))

    # Loop imaging planes
    options_per_plane = np.load(general_options_save_file, allow_pickle=True)
    for plane in range(Im.nplanes):

        # Do registration
        t = time.time()
        print("\nProcessing plane {}".format(plane))
        options_per_plane[plane] = register.register_binary(options_per_plane[plane])
        np.save(general_options_save_file, options_per_plane)
        print(" .. done ({:0.1f} s)".format((time.time()-t)))

        # Update the cropping parameters with the lightleak exclusion zone
        options_per_plane[plane]["xrange"][0] = np.max([options_per_plane[plane]["xrange"][0], preprocsettings["im_xrange"][0]])
        options_per_plane[plane]["xrange"][1] = np.min([options_per_plane[plane]["xrange"][1], preprocsettings["im_xrange"][1]])

        # Do cell detection
        t=time.time()
        options_per_plane[plane] = extract.detect_and_extract(options_per_plane[plane])
        plane_file_path = options_per_plane[plane]['save_path']
        print(" .. done ({:0.1f} s)".format((time.time()-t)))

        # Deconvolution
        t=time.time()
        F = np.load(os.path.join(plane_file_path,'F.npy'))
        Fneuropil = np.load(os.path.join(plane_file_path,'Fneu.npy'))
        dF = F - options_per_plane[plane]['neucoeff']*Fneuropil
        dF = dcnv.preprocess(dF,options_per_plane[plane])
        spikes = dcnv.oasis(dF, options_per_plane[plane])
        np.save(os.path.join(options_per_plane[plane]['save_path'],'spks.npy'), spikes)
        print(" .. done ({:0.1f} s)".format((time.time()-t)))

    # Save options and settings
    np.save(general_options_save_file, options_per_plane)
    np.save(preprocsettings_save_file, preprocsettings)
