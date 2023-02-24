import os
import cv2
import filetype

import warnings as warn
warn.filterwarnings("ignore")

import delg_landmark_retrieval as classify
# -------------------------------------------------------------------------------------------------------
# Detect and recognize landmark on either of the left or right image using DELG landmark detection model
# --------------------------------------------------------------------------------------------------------

# get pre-trainned  delg model
# TF_MODEL_URL = 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_asia_V1/1'
# LABEL_MAP_URL = 'https://www.gstatic.com/aihub/tfhub/labelmaps/landmarks_classifier_asia_V1_label_map.csv'
TF_MODEL_URL = 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_north_america_V1/1'
LABEL_MAP_URL = 'https://www.gstatic.com/aihub/tfhub/labelmaps/landmarks_classifier_north_america_V1_label_map.csv'

# import pandas as pd
# df = pd.read_csv(LABEL_MAP_URL)
#
# df.head()


###resize image to required dimension
# IMAGE_SHAPE = (321, 321)
def resize_img(img):
    '''
        :param:
        :img: image location

    '''
    width = 321
    height = 321
    dsize = (width, height)
    img_gray = cv2.imread(img, 0)
    img_rbg = cv2.imread(img, 1)

    # resize image
    mg_gray_resized = cv2.resize(img_gray, dsize)
    rbg_img_resized = cv2.resize(img_rbg, dsize)
    return rbg_img_resized, mg_gray_resized

img_path_left = "dataset/images/stereoL/"
img_path_right = "dataset/images/stereoR/"

# imgLeft = mpimg.imread(img_path_left + 'imgL1.png')
imgLeft = img_path_left + 'imgL1.png'
imgRight = img_path_right + 'imgR1.png'


path_to_stereo_images = "dataset/images/stereoL/"
def show_result(path_to_stereo_images):
    for filename in os.listdir(path_to_stereo_images):
        image = os.path.join(path_to_stereo_images, filename)
        if filetype.is_image(image):
            # print(image)
            cv2.imshow("Stereo Left", image)
            break
    #     imgL_rbg, imgL_gray = resize_img(imgLeft)
    #     imgR_rbg, imgR_gray = resize_img(imgRight)
    #
    # landmark_detected1 = classify.classify_image(imgL_rbg, TF_MODEL_URL, LABEL_MAP_URL)
    # landmark_detected2 = classify.classify_image(imgR_rbg, TF_MODEL_URL, LABEL_MAP_URL)
    #
    # print(landmark_detected1, landmark_detected2)
show_result(path_to_stereo_images)
