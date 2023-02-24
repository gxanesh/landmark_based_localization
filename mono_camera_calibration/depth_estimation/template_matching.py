import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib import gridspec
from numpy import random
from sklearn import datasets


def ShowDisparity(imgLeft,imgRight,bSize):
    '''
        imgLeft: left image in graysccale
        imgRight: right image in grayscale
    '''
    # Initialize the stereo block matching object
    stereo = cv2.StereoBM_create(numDisparities=32, blockSize=bSize)
    # grayscale image
    # imgLeft = cv2.imread('tsukuba_l.png', 0)
    # imgRight = cv2.imread('tsukuba_l.png', 0)
    # Compute the disparity image
    disparity = stereo.compute(imgLeft, imgRight)

    # Normalize the image for representation
    min = disparity.min()
    max = disparity.max()
    disparity = np.uint8(255 * (disparity - min) / (max - min))

    # Plot the result
    return disparity
