#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Command line script to run image and roi processing of calcium imaging data using suite2p

python preprocessing -m datapath settingspath

Created on Sat Feb 22, 2020

@author: pgoltstein
"""

# Imports
from . import preproc
import argparse


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Arguments

parser = argparse.ArgumentParser( description = "Runs suite2p image and ROI processing. \n (written by Pieter Goltstein - February 2020)")
parser.add_argument('-d', '--datapath', type=str, default=None, help='path to the folder where data are located')
parser.add_argument('-s', '--settingspath', type=str, default=None, help='path to the folder where settingsfiles are located')
args = parser.parse_args()


#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
# Start preprocessing script

preproc.run_preprocessing( datapath=args.datapath, settingspath=args.settingspath )
