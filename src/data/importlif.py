def boom(gfp_file, tom_file):
    import cv2
    gfp = gfp_file
    tom = tom_file
    gfp_proc, gfp_bin = preproc(gfp)
    tom_proc, tom_bin = preproc(tom)
    gfp_blobs = cellcount_2d(gfp_bin)
    tom_blobs = cellcount_2d(tom_bin)
    gfp_means = lumcalc(gfp_proc, gfp_blobs)
    tom_means = lumcalc(tom_proc,tom_blobs)
    gfp_circ = circleblobs_2d(gfp_blobs, gfp, gfp_means)
    tom_circ = circleblobs_2d(tom_blobs, tom, tom_means)
    tom_im,gfp_im,circ_in_tom,circ_in_gfp=comparechannels(gfp_circ,gfp_bin,gfp_blobs,tom_circ,tom_bin,tom_blobs)
    return(gfp_im, tom_im)
    
    
#########################################
## importlif is used for LIF files with only 1 series per file, and 2 channels 
## GFP and TOM
def importlif (file):
    import read_lif as rl
    reader = rl.Reader(file)
    series = reader.getSeries()
    chosen = series[0]
    image_GFP = chosen.getFrame(T=0, channel=0)
    image_TOM = chosen.getFrame(T=0, channel=1)
    return(image_GFP, image_TOM)

def preproc (image):
    import cv2 
    import numpy as np
    from skimage import color
    j = color.rgb2gray(image)
    j = j*(255/np.max(j))
    j = j.astype(np.uint8)
    imx = image.shape[0]
    imy = image.shape[1]
    for x in range(imx):
            for y in range(imy):
                if j[x,y] <35:
                    j[x,y] = 0
    im_blur = cv2.GaussianBlur(j,(301,301),0)
    im_den = cv2.fastNlMeansDenoising(j,None,10,7,31)
    for x in range(imx):
        for y in range(imy):
            if im_blur[x,y] < im_den[x,y]:
                im_den[x,y] = im_den[x,y] - im_blur[x,y]
            else:
                im_den[x,y] = 0
    im_binary = cv2.threshold(im_den,40,255, cv2.THRESH_BINARY)
    im_bin = im_binary[1]
    return(im_den, im_bin)
                        
def cellcount(procd_im):
    from skimage.feature import blob_log
    a = []
    zplanes = procd_im.shape[2]
    for z in range (zplanes):
        j = procd_im[:,:,z]
        blobs = blob_log(j, min_sigma=8, max_sigma=12, threshold=.07)
        a.append(blobs)
    return(a)
    
def cellcount_2d(procd_im):
    from skimage.feature import blob_log
    blobs = blob_log(procd_im, min_sigma=10, max_sigma=12, threshold=.05)
    #print(len(blobs))
    return(blobs)
 
    
    
##calculates mean luminance of each cell from cellcount
def lumcalc(procd_im_a, blobs):
    import numpy as np
    from skimage import color
    means = []
    procd_im = color.rgb2gray(procd_im_a)
    for blob in range(0,blobs.shape[0]):
        mask=np.zeros(procd_im.shape)
        r = int(blobs[blob,2])
        a = blobs[blob,0]
        b = blobs[blob,1]
        nx = procd_im.shape[0]
        ny = procd_im.shape[1]
        y,x = np.ogrid[-a:nx-a, -b:ny-b]
        mask = (x*x + y*y <= r*r)*1.0
        masked_im = mask * procd_im
        lum = sum(sum(masked_im))/sum(sum(mask))
        means.append(lum)
    return(means)

def circleblobs(blobs, image):
    import numpy as np
    import cv2
    from skimage import color
    zplanes = image.shape[2]
    sendback = []
    for z in range(zplanes):
        im = color.gray2rgb(image[:,:,z])
        blob_z = np.array(blobs[z])
        how_many_blobs=list(range(blob_z.shape[0]))
        for blob_num in how_many_blobs:
            x=int(blob_z[blob_num,0])
            y=int(blob_z[blob_num,1])
            r=int(blob_z[blob_num,2])
            cv2.circle(im,(y,x), r, (255,255,255), 1)
        im_conv = color.rgb2gray(im)
        sendback.append(im_conv)
    return(sendback)
    
def circleblobs_conditional(blobs, image, means):
    import numpy as np
    import cv2
    from skimage import color
    im = color.gray2rgb(image)
    blob_z = np.array(blobs)
    how_many_blobs=list(range(blob_z.shape[0]))
    avg = np.mean(means)
    count = 0
    for blob_num in how_many_blobs:
        if means[blob_num] > 15:
            x=int(blob_z[blob_num,0])
            y=int(blob_z[blob_num,1])
            r=int(blob_z[blob_num,2])
            cv2.circle(im,(y,x), r, (0,255,0), 1)
            count = count + 1
    #print (count)
    return(im)
    
def circleblobs_2d(blobs, image, r,g,b):
    import numpy as np
    import cv2
    from skimage import color
    im = color.gray2rgb(image)
    blob_z = np.array(blobs)
    how_many_blobs=list(range(blob_z.shape[0]))
    count = 0
    for blob_num in how_many_blobs:
        x=int(blob_z[blob_num,0])
        y=int(blob_z[blob_num,1])
        rad=int(blob_z[blob_num, 3])
        cv2.circle(im,(y,x), rad, (r,g,b), 1)
        count = count + 1
    #print (count)
    return(im, how_many_blobs)
    
def comparechannels(gfp_circled, gfpblobs, gfp_means, tom_circled, tomblobs, tom_means):
##imports
    import numpy as np
    import cv2
    circ_in_tom = []
    for blob in range(0,gfpblobs.shape[0]):
        circ_in_tom.append(gfpblobs[blob,:])
    circ_in_tom = np.array(circ_in_tom)
    gfp_means_len = len(circ_in_tom)
    for blob in range(gfp_means_len):
        x=int(circ_in_tom[blob,0])
        y=int(circ_in_tom[blob,1])
        r=int(circ_in_tom[blob,3])
        cv2.circle(tom_circled,(y,x), r, (0,255,0), 2)    
        circ_in_gfp = []
    for blob in range(0,tomblobs.shape[0]):
        circ_in_gfp.append(tomblobs[blob,:])
    circ_in_gfp = np.array(circ_in_gfp)
    tom_means_len = len(circ_in_gfp)
    for blob in range(tom_means_len):
        x=int(circ_in_gfp[blob,0])
        y=int(circ_in_gfp[blob,1])
        r=int(circ_in_gfp[blob,3])
        cv2.circle(gfp_circled,(y,x), r, (0,0,255), 2)   
    
    return()

    
    
