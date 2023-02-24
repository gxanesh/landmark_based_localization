import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# from matplotlib import gridspec
# from numpy import random
# from sklearn import datasets
# %matplotlib inline

import warnings as warn
warn.filterwarnings("ignore")

# imaage: St. Andrew's Tower https://live.staticflickr.com/65535/46935273825_2cfbee5881_h.jpg
img_path_left = "dataset/images/stereoL/"
img_path_right = "dataset/images/stereoR/"

imgLeft = mpimg.imread(img_path_left + 'imgL1.png')
imgRight = mpimg.imread(img_path_right + 'imgR1.png')

plt.figure(figsize=(10,5))
plt.subplot(1,2,1)
plt.imshow(imgLeft)
plt.axis('off')
plt.subplot(1,2,2)
plt.imshow(imgRight)
plt.axis('off')
plt.show()
