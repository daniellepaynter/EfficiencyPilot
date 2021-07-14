#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

This script tests the module suite2pdata.

Created on Thursday 16 July 2020

@author: pgoltstein
"""

import os, glob
import matplotlib.pyplot as plt
import suite2pdata
import argparse


# =============================================================================
# Arguments

parser = argparse.ArgumentParser( description = "This script tests the module suite2pdata.\n (written by Pieter Goltstein - July 2020)")
parser.add_argument('filepath', type=str, help= 'path to the folder holding the image stack')
args = parser.parse_args()


# =============================================================================
# Code


print("\nTesting suite2pdata:")
S2p = suite2pdata.Suite2pData(args.filepath)
print(S2p)

print("S2p.nplanes = {}".format(S2p.nplanes))
spikes = S2p.spikes
print("spikes.shape = {}".format(spikes.shape))
S2p.plane = 2
spikes = S2p.spikes
print("spikes.shape = {}".format(spikes.shape))

x,y = S2p.x,S2p.y
plane = S2p.plane
nid = S2p.neurons
for roi in range(5):
    print("ROI {}: x={},y={}, plane={}, id={}".format(roi, x[roi], y[roi], plane, nid[roi]))

S2p.select_neurons("iscell")
S2p.select_neurons("isnotcell")
S2p.select_neurons("iscell_p_larger_than",0.8)
S2p.select_neurons("iscell_p_smaller_than",0.5)
spikes = S2p.spikes
print("spikes.shape = {}".format(spikes.shape))

print("\nDone testing\n")
