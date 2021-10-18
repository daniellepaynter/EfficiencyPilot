# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 14:07:12 2021

@author: dpaynter
"""
### Set the variables: 
mouse = 'DP_210224C'
num_locs = 12
dates = ["210315",
"210318",
"210323",
"210325",
"210329",
]

### Imports:
import os

locs = ['740', '760', '780', '800', '820', '840', '860', '880', '900', '910', '920', '930']

ch1_folder = os.path.join(r"I:/Danielle Paynter/InVivoTTTPilots/efficiency_pilot/data/interim/Intensify3D_layout", mouse, "Ch1")
#ch2_folder = os.path.join(r"I:/Danielle Paynter/InVivoTTTPilots/efficiency_pilot/data/interim/Intensify3D_layout", mouse, "Ch2")

#os.makedirs(ch1_folder)
#os.makedirs(ch2_folder)

for loc in range(num_locs):
    for date in range(len(dates)):
        os.makedirs(os.path.join(ch1_folder, locs[loc], dates[date]))
        #os.makedirs(os.path.join(ch2_folder, locs[loc], dates[date]))

