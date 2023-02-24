import numpy as np
import cv2
import time
import os

import warnings as warn
warn.filterwarnings("ignore")

print("Checking the right and left camera:")

# Check for left and right camera IDs
CamL_id = 0
CamR_id = 2

#board Dimension

CHESS_BOARD_DIM = (8, 6)

# stopping criteria for corner detection
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# detect checker board
def detect_checker_board(image, grayImage, criteria, boardDimension):
    ret, corners = cv2.findChessboardCorners(grayImage, boardDimension)
    if ret == True:
        corners1 = cv2.cornerSubPix(grayImage, corners, (3, 3), (-1, -1), criteria)
        image = cv2.drawChessboardCorners(image, boardDimension, corners1, ret)

    return image, ret

#access web cam to capture frames

CamL= cv2.VideoCapture(CamL_id)
CamR= cv2.VideoCapture(CamR_id)

output_path = "./data/"
image_dir_path_left = output_path + "images/stereoL/"
image_dir_path_right = output_path + "images/stereoR/"

# check directory to store stereo images
CHECK_DIR_L = os.path.isdir(image_dir_path_left)
CHECK_DIR_R = os.path.isdir(image_dir_path_right)

# print(image_dir_path_left,image_dir_path_right)
# if directory does not exist createq
if not CHECK_DIR_L and not CHECK_DIR_R:
    os.makedirs(image_dir_path_left)
    os.makedirs(image_dir_path_right)

    print(f'{image_dir_path_left, image_dir_path_right} Directories are created.')

else:
    print(f'{image_dir_path_left, image_dir_path_right} Directories already Exist.')


start = time.time()
T = 5
count = 0

while True:
    timer = T - int(time.time() - start)

    retL, frameL= CamL.read()
    retR, frameR= CamR.read()
    # if frameR is None:
    #     break
    frameL_temp = frameL.copy()
    # if frameR is None:
    #     break
    frameR_temp = frameR.copy()

    cv2.putText(
        frameL,
        f"saved_imgL : {count}",
        (30, 40),
        cv2.FONT_HERSHEY_PLAIN,
        1.4,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        frameR,
        f"saved_imgR : {count}",
        (30, 40),
        cv2.FONT_HERSHEY_PLAIN,
        1.4,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    # cv.imshow("frame", frame)
    # cv.imshow("copyFrame", copyFrame)



    grayL= cv2.cvtColor(frameL,cv2.COLOR_BGR2GRAY)
    grayR= cv2.cvtColor(frameR,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    # retL, cornersL = cv2.findChessboardCorners(grayL,(8,6),None)
    # retR, cornersR = cv2.findChessboardCorners(grayR,(8,6),None)
    _, retL = detect_checker_board(frameL, grayL, criteria, CHESS_BOARD_DIM)
    _, retR = detect_checker_board(frameR, grayR, criteria, CHESS_BOARD_DIM)

    # cv2.imshow('Board detected',frameL)
    cv2.imshow('imgL',frameL)
    cv2.imshow('imgR',frameR)

    # If corners are detected in left and right image then we save it.
    # print(retL,retR)
    if (retL == True) and (retR == True) and timer <=0:
        count+=1
        cv2.imwrite(image_dir_path_left+'img%d.png'%count,frameL_temp)
        cv2.imwrite(image_dir_path_right+'img%d.png'%count,frameR_temp)

        print(f"saved image number {count}")

    if timer <=0:
        start = time.time()

    # Press esc to exit
    if (cv2.waitKey(1) & 0xFF == ord('q')) or (cv2.waitKey(1) & 0xFF == 27):
        print("Closing the cameras!")
        break

# Release the Cameras
CamR.release()
CamL.release()
cv2.destroyAllWindows()
