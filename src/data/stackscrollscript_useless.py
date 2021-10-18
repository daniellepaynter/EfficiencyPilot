def stack_scroll(im_directory, im_title):
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
    im_stack = np.transpose(im_stack, axes=[2, 1, 0])
    
    return im_stack


im3_stack = stack_scroll(r'I:\Danielle Paynter\InVivoTTTPilots\efficiency_pilot\data\processed\DP_210519A\210624\loc4\2_smooth_contrast_FIJI\Ch1', 'hehe')
