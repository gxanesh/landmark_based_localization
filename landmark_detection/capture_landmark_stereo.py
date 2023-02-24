import cv2
import time
import os
import sys

sys.path.append('/usr/local/home/gs37r/Ganesh/Research Project Main/Implementation/landmark_based_localization/stereo_vision_method')

import warnings as warn
warn.filterwarnings("ignore")

import landmark_detection.dataset.images.delete_stereo_images as delete

# print("Checking the right and left camera:")

# Check for left and right camera IDs
# print(os.getcwd())
def capture_stereo(cam_ids):
    # CamL_id = 0
    # CamR_id = 2
    CamL_id = cam_ids[0]
    CamR_id = cam_ids[1]

    #access web cam to capture frames

    CamL= cv2.VideoCapture(CamL_id)
    CamR= cv2.VideoCapture(CamR_id)

    # output_path = "/dataset/"
    image_dir_path_left = "./dataset/images/stereoL/"
    image_dir_path_right = "./dataset/images/stereoR/"
    image_dir_path_stereoCombined = "./dataset/images/stereoCombined/"

    # check directory to store stereo images
    CHECK_DIR_L = os.path.isdir(image_dir_path_left)
    CHECK_DIR_R = os.path.isdir(image_dir_path_right)

    # if directory does not exist createq
    if not CHECK_DIR_L and not CHECK_DIR_R:
        os.makedirs(image_dir_path_left)
        os.makedirs(image_dir_path_right)
        os.makedirs(image_dir_path_stereoCombined)

        # print(f'{image_dir_path_left, image_dir_path_right,image_dir_path_stereoCombined} Directories are created.')

    else:
        # print(f'{image_dir_path_left, image_dir_path_right,image_dir_path_stereoCombined} Directories already Exist.')
        print("Deleting previous stereo images...")
        format = '.png'
        delete.delete_all_stereo("dataset/images/stereoL/", format)
        delete.delete_all_stereo("dataset/images/stereoR/", format)
        delete.delete_all_stereo("dataset/images/stereoCombined/", format)


    start = time.time()
    T = 5
    count = 0

    while True:
        timer = T - int(time.time() - start)

        retL, frameL= CamL.read()
        retR, frameR= CamR.read()

        # cv2.putText(
        #     frameL,
        #     f"saved_imgL : {count}",
        #     (30, 40),
        #     cv2.FONT_HERSHEY_PLAIN,
        #     1.4,
        #     (0, 255, 0),
        #     2,
        #     cv2.LINE_AA,
        # )
        #
        # cv2.putText(
        #     frameR,
        #     f"saved_imgR : {count}",
        #     (30, 40),
        #     cv2.FONT_HERSHEY_PLAIN,
        #     1.4,
        #     (0, 255, 0),
        #     2,
        #     cv2.LINE_AA,
        # )
        # cv2.imshow('Board detected',frameL)
        # cv2.imshow('imgL',frameL)
        # cv2.imshow('imgR',frameR)

        # cv2.imwrite(image_dir_path_stereoCombined+'imgLR%d.png'%count,frameR)


        # print(f"saved image number {count}")

        if timer <=0:
            count += 1
            landmark_folder_name = 'l1'

            # CHECK_DIR_L = os.path.isdir(image_dir_path_left + landmark_folder_name)
            # CHECK_DIR_R = os.path.isdir(image_dir_path_right + landmark_folder_name)
            #
            # # if directory for new landmark does not exist then createq
            # if not CHECK_DIR_L and not CHECK_DIR_R:
            #     #add new directory when new landmark is detected. save the images of each new landmarks on the corrosponding folder
            #     os.makedirs(image_dir_path_left + landmark_folder_name )
            #     os.makedirs(image_dir_path_right + landmark_folder_name)

            cv2.imwrite("dataset/images/stereoL/" + 'imgL%d.png' % count, frameL)
            cv2.imwrite("dataset/images/stereoR/" + 'imgR%d.png' % count, frameR)
            print("stereo image saved")
            start = time.time()

        dir_path = image_dir_path_left
        no_of_images = len([entry for entry in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, entry))])

        ###close the camera when two photos are taken or 'q' is pressed
        if (cv2.waitKey(1) & 0xFF == ord('q')) or (no_of_images == 1):
            print("Closing the cameras!")
            break
    # Release the Cameras
    CamR.release()
    CamL.release()
    cv2.destroyAllWindows()

