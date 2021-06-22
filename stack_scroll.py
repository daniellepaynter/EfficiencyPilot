# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 22:30:44 2021

Loads all images in "im_directory" and displays them as a stack that can be 
scrolled through using the mouse wheel.

Based largely off matplotlib's Image Slices Viewer
(https://matplotlib.org/stable/gallery/event_handling/image_slices_viewer.html)

m
@author: dpaynter
"""
# Set directory to get images from, and title of images
im_directory = r'C:\Users\dpaynter\Dropbox\Danielle-Pieter-shared-folder\210617_sample2Ptiffs'
im_title = '210617_sampleloc'

# Imports
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2

# Define a list to store the image arrays
im_stack = []

# Read in all images; append one plane to im_stack
for nr, filename in enumerate(os.listdir(im_directory)):
    if filename.endswith('.tiff'):
        im = cv2.imread(os.path.join(im_directory, filename))
        im = im[:, :, 1]
        im_stack.append(im)
        
# Convert im_stack to an array and make the axes x, y, z
im_stack = np.array(im_stack)
im_stack = np.transpose(im_stack, axes=[2,1,0])


class IndexTracker():
    """Class that holds  """
    def __init__(self, ax, stack, im_title):
        self.ax = ax
        self.ax.set_title(im_title)
        self.stack = stack
        self.rows, self.cols, self.slices = stack.shape
        self.ind = self.slices//2

        self.im = ax.imshow(self.stack[:, :, self.ind])
        self.update()

    def on_scroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.stack[:, :, self.ind])
        self.ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()


fig, ax = plt.subplots(1, 1)


tracker = IndexTracker(ax, im_stack, im_title)


fig.canvas.mpl_connect('scroll_event', tracker.on_scroll)
plt.show()