# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 13:49:29 2021

@author: dpaynter
"""

import cv2
import numpy as np

max_features = 1000
good_match_percent = .1

def align_images(im1, im2):



  # Extract location of good matches

   points1 = np.zeros((len(matches), 2), dtype=np.float32)
   points2 = np.zeros((len(matches), 2), dtype=np.float32)


  # Find homography

   h, mask = cv2.findHomography(points1, points2)
  # Use homography
   height, width, channels = im2.shape
   im1Reg = cv2.warpPerspective(im1, h, (width, height))

   return im1Reg, h, matches, mask


# Registered image will be resotred in imReg.
# The estimated homography will be stored in h.

imReg, h, matches, mask = align_images(im1, im2)

 
# Write aligned image to disk.

outFilename = r"C:\Users\dpaynter\Desktop\tests_210921\aligned.jpg"

print("Saving aligned image : ", outFilename);
cv2.imwrite(outFilename, imReg)
 
# Print estimated homograph
print("Estimated homography : \n",  h)
print("Mean of distances: \n", np.mean([matches[count].distance for count, val in enumerate(matches)]))
print("Num matches: \n", len(matches))