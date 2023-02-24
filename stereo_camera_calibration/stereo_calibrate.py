import numpy as np 
import cv2
import os
from tqdm import tqdm

import warnings as warn
warn.filterwarnings("ignore")

# Set the path to the images captured by the left and right cameras


# print(os.path.relpath('img1.png'))

CHESS_BOARD_DIM = (8, 6)

# The size of Square in the checker board.
SQUARE_SIZE = 25  # millimeters

print("Extracting image coordinates of respective 3D pattern ....\n")

# Termination criteria for refining the detected corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0) 3*3 matrix
obj_3D = np.zeros((CHESS_BOARD_DIM[0] * CHESS_BOARD_DIM[1], 3), np.float32)

obj_3D[:, :2] = np.mgrid[0 : CHESS_BOARD_DIM[0], 0 : CHESS_BOARD_DIM[1]].T.reshape(
    -1, 2
)
obj_3D *= SQUARE_SIZE
# print(obj_3D)

# Arrays to store object points and image points from all the images.
obj_points_3D = []  # 3d point in real world space
img_pointsL_2D = []  # 2d points in image plane.
img_pointsR_2D = []  # 2d points in image plane.

# image_dir_path = "images"
image_dir_pathL = "./data/images/stereoL/"
image_dir_pathR = "./data/images/stereoL/"

# files = os.listdir(image_dir_path)

for i in tqdm(range(1,16)):
	imgL = cv2.imread(image_dir_pathL+"img%d.png"%i)
	imgR = cv2.imread(image_dir_pathR+"img%d.png"%i)
	imgL_gray = cv2.imread(image_dir_pathL+"img%d.png"%i,0)
	imgR_gray = cv2.imread(image_dir_pathR+"img%d.png"%i,0)

	# print(imgL)
	outputL = imgL.copy()
	outputR = imgR.copy()

	retR, cornersR =  cv2.findChessboardCorners(outputR,(8,6),None)
	retL, cornersL = cv2.findChessboardCorners(outputL,(8,6),None)

	if retR and retL:
		obj_points_3D.append(obj_3D)
		cornersR2 = cv2.cornerSubPix(imgR_gray,cornersR,(3,3),(-1,-1),criteria)
		cornersL2 = cv2.cornerSubPix(imgL_gray,cornersL,(3,3),(-1,-1),criteria)
		cv2.drawChessboardCorners(outputR,(8,6),cornersR2,retR)
		cv2.drawChessboardCorners(outputL,(8,6),cornersL2,retL)
		# cv2.imshow('cornersR',outputR)
		# cv2.imshow('cornersL',outputL)
		# cv2.waitKey(0)

		img_pointsL_2D.append(cornersL2)
		img_pointsR_2D.append(cornersR2)

cv2.destroyAllWindows()
print("Calculating left camera parameters ... ")
# Calibrating left camera
'''
	ret: is board detected
	mtx: essential matrix with intrinsic paramaters
	dist:   distortion coefficients
	rvecs : rotational vectors(matrix)
	tvecs: transational vectors(matrix)
	
'''
retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(obj_points_3D,img_pointsL_2D,imgL_gray.shape[::-1],None,None)
hL,wL= imgL_gray.shape[:2]
#is used to use different resolutions from the same camera with the same calibration(if u want to crop change(w,h))

new_mtxL, roiL= cv2.getOptimalNewCameraMatrix(mtxL,distL,(wL,hL),1,(wL,hL))

print("Calculating right camera parameters ... ")
# Calibrating right camera
retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(obj_points_3D,img_pointsR_2D,imgR_gray.shape[::-1],None,None)
hR,wR= imgR_gray.shape[:2]
alpha = 1 #use the value between [0,1]
new_mtxR, roiR= cv2.getOptimalNewCameraMatrix(mtxR,distR,(wR,hR),alpha,(wR,hR))


print("Stereo calibration .....")
flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
# Here we fix the intrinsic camara matrixes so that only Rot, Trns, Emat and Fmat are calculated.
# Hence intrinsic parameters are the same

criteria_stereo= (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


# This step is performed to transformation between the two cameras and calculate Essential and Fundamenatl matrix
retS, new_mtxL, distL, new_mtxR, distR, Rot, Trns, Emat, Fmat = cv2.stereoCalibrate(obj_points_3D,
                                                          img_pointsL_2D,
                                                          img_pointsR_2D,
                                                          new_mtxL,
                                                          distL,
                                                          new_mtxR,
                                                          distR,
                                                          imgL_gray.shape[::-1],
                                                          criteria_stereo,
                                                          flags)

# Once we know the transformation between the two cameras we can perform stereo rectification
# StereoRectify function
rectify_scale= 1 # if 0 image croped, if 1 image not croped
rect_l, rect_r, proj_mat_l, proj_mat_r, Q, roiL, roiR= cv2.stereoRectify(new_mtxL, distL, new_mtxR, distR,
                                                 imgL_gray.shape[::-1], Rot, Trns,
                                                 rectify_scale,(0,0))

# Use the rotation matrixes for stereo rectification and camera intrinsics for undistorting the image
# Compute the rectification map (mapping between the original image pixels and
# their transformed values after applying rectification and undistortion) for left and right camera frames
Left_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxL, distL, rect_l, proj_mat_l,
                                             imgL_gray.shape[::-1], cv2.CV_16SC2)
Right_Stereo_Map= cv2.initUndistortRectifyMap(new_mtxR, distR, rect_r, proj_mat_r,
                                              imgR_gray.shape[::-1], cv2.CV_16SC2)
# print("Left_Stereo_Map: ",Left_Stereo_Map[0])
# print("Right_Stereo_Map: ",Right_Stereo_Map[0])


print("Saving paraeters....")
cv_file = cv2.FileStorage("../stereo_camera_calibration/data/calibration_param.xml", cv2.FILE_STORAGE_WRITE)
cv_file.write("Left_Stereo_Map_x",Left_Stereo_Map[0])
cv_file.write("Left_Stereo_Map_y",Left_Stereo_Map[1])
cv_file.write("Right_Stereo_Map_x",Right_Stereo_Map[0])
cv_file.write("Right_Stereo_Map_y",Right_Stereo_Map[1])

print("Calibtation parameter saved to stereo_camera_calibration/data directory!")
cv_file.release()
