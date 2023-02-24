import time

import numpy as np
import cv2
import os
import json
# import keyboard
# import filetype
# from sys import exit

import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


sys.path.append(
    '/usr/local/home/gs37r/Ganesh/Research Project Main/Implementation/landmark_based_localization/stereo_vision_method')
# sys.path.append('/usr/local/home/gs37r/Ganesh/Research Project Main/Implementation/landmark_based_localization/stereo_vision_method')

import localization.update_json as json_data
import localization.convert_coordinates as convert
import landmark_detection.delg_landmark_retrieval as delg
import landmark_detection.get_landmark_location as lloc
import landmark_detection.capture_landmark_stereo as capture
import stereo_camera_calibration.calibrated_stereo_vision as distance


# Get landmark coordinates from landmark names
def getLandmarksCoords():
    # get landmarks as the result of object detection
    # dummy values
    l1 = [4, 7]
    l2 = [7, 9]
    l3 = [9, 13]
    landmark = {'l1': l1, 'l2': l2, 'l3': l3}
    return landmark


def get_XYCoords(landmark):
    # landmark is dict of landmarks
    landmark_XCoords = []
    landmark_YCoords = []
    arr_size = len(landmark)
    for k, v in landmark.items():
        landmark_XCoords.append(v[0])
        landmark_YCoords.append(v[1])
    return np.array(landmark_XCoords), np.array(landmark_YCoords)


def create_json():
    # #obtain average depth fro mdepth calculation
    output_path = "./data/"
    # check directory to store stereo images
    CHECK_DIR = os.path.isdir(output_path)

    # print(image_dir_path_left,image_dir_path_right)
    # if directory does not exist create
    if not CHECK_DIR:
        os.makedirs(output_path)
        print(f'{output_path} Directory is created.')

    else:
        print(f'{output_path} Directory already exists!')
    # Data to be written
    landmarks_detected = {
        "id" : [],
        "name":[],
        "location": [],
        "distance": [],
        "timestamp": []
    }

    # Serializing json
    landmark_json_object = json.dumps(landmarks_detected)

    # Writing to sample.json
    with open(output_path + "landmark_data.json", "w") as outfile:
        outfile.write(landmark_json_object)

def get_node_location(json_file):
    '''

    :param landmark_data: landmark json file containing landmark information
    :return: current position of node/camera holder
    '''
    # filepath = './data/landmark_data.json'
    filepath = json_file
    with open(filepath) as json_file:
        landmark_data = json.load(json_file)

    landmark_name = landmark_data['name']
    landmark_location = landmark_data['location']
    landmark_distance = landmark_data['distance']

    x1 = landmark_location[0][0]
    y1 = landmark_location[0][1]
    x2 = landmark_location[1][0]
    y2 =landmark_location[1][1]
    x3 =landmark_location[2][0]
    y3 =landmark_location[2][1]
    #
    # print(landmark_location[0][0])
    d1 = landmark_distance[0]
    d2 = landmark_distance[1]
    d3 = landmark_distance[2]
    # print(landmark_name,landmark_location,landmark_distance)
    # print(x1,y1,x2,y2,x3,y3)
    # print(d1,d2,d3)
    r1 = [2 * (x1 - x3), 2 * (y1 - y3)]
    r2 = [2 * (x2 - x3), 2 * (y2 - y3)]
    AT_A = np.vstack([r1, r2])
    # AT_A

    AT_A_inverse = np.linalg.inv(AT_A)
    # AT_A_inverse
    r2 = [x1 * x1 - x3 * x3 + y1 * y1 - y3 * y3 + d3 * d3 - d1 * d1]
    r3 = [x2 * x2 - x3 * x3 + y2 * y2 - y3 * y3 + d3 * d3 - d1 * d2]
    AT_Y = np.vstack([r2, r3])
    # # # AT_Y
    #
    current_position_acc = np.dot(AT_A_inverse, AT_Y)
    # current_position_approx = np.ceil(np.dot(AT_A_inverse,AT_Y))
    # print('Current position of Node is:', current_position_acc)
    return current_position_acc


def resize_img(img):
    '''
        ###resize image to required dimension
        # IMAGE_SHAPE = (321, 321)
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


def get_data():
    '''
    get json data of each landmark
    :return:
    '''
    run = 0
    cam_ids = [0, 2]

    capture.capture_stereo(cam_ids)

    # 2 detect and retrieve landmark from input frames
    # -------------------------------------------------------------------------------------------------------
    # Detect and recognize landmark on either of the left or right image using DELG landmark detection model
    # --------------------------------------------------------------------------------------------------------

    # get pre-trainned  delg model
    TF_MODEL_URL = 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_asia_V1/1'
    LABEL_MAP_URL = 'https://www.gstatic.com/aihub/tfhub/labelmaps/landmarks_classifier_asia_V1_label_map.csv'
    TF_MODEL_URL = 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_north_america_V1/1'
    LABEL_MAP_URL = 'https://www.gstatic.com/aihub/tfhub/labelmaps/landmarks_classifier_north_america_V1_label_map.csv'

    path_to_stereo_images = "./dataset/images/stereoL/"  # here we use images from left stereo camera for landmark detection

    for filename in os.listdir(path_to_stereo_images):
        image = os.path.join(path_to_stereo_images, filename)
        # if filetype.is_image(image):
        #     # print(image)
        #     cv2.imshow("Stereo Left", image)
        #     break
    imgL_rbg, imgL_gray = resize_img(image)

    landmark_detected = delg.retrieve_landmark(imgL_rbg, TF_MODEL_URL, LABEL_MAP_URL)
    # update new  detected landmark name
    json_data.update_json(name=landmark_detected)

    # 3 get name of landmark and update json
    print("landmark_detected:", landmark_detected)

    # 4 get location of landmark and update json
    landmark_loc = lloc.get_location(landmark_detected)
    json_data.update_json(location=landmark_loc)
    print("landmark_loc: ", landmark_loc)

    ##distance calculation
    # 5 get distance and update json
    # for i in range(3):
    avg_depth =  distance.get_distance_to_landmark(cam_ids)
    json_data.update_json(distance=round(avg_depth, 1), timestamp=time.time())

if __name__ == "__main__":
    # Runtime algorithm steps
    # 1 capture input frames and save file name: capture_landmark_stereo
    #set countered to stopped landmark detection when three landmarks are detected
    c = 0
    # clear old json or create new json file if doesnt exist
    json_data.clear_json()
    while c<3:
        if (cv2.waitKey(1) & 0xFF == ord('a')):
            break
        else:
            get_data()
            c+=1

    # # 6 Apply least square to get node location
    json_data =  './data/landmark_data.json'
    current_location = get_node_location(json_data).tolist()
    # lat = current_location[0]
    # lon  =  current_location[1]
    current =  convert.latlon_to_xyz(round(current_location[0][0],2),round(current_location[0][0],2))
    print("current_location latitude longitude",current_location)
    print("current_location X, Y: ", current)
