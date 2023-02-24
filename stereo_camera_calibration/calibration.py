import cv2

# Camera parameters to undistort and rectify images
cv_file = cv2.FileStorage()
cv_file.open('./data/calibration_param.xml', cv2.FileStorage_READ)


# print(cv_file)
stereoMapL_x = cv_file.getNode('Left_Stereo_Map_x').mat()
stereoMapL_y = cv_file.getNode('Left_Stereo_Map_y').mat()
stereoMapR_x = cv_file.getNode('Right_Stereo_Map_x').mat()
stereoMapR_y = cv_file.getNode('Right_Stereo_Map_y').mat()

# print("stereoMapL_x ", stereoMapL_x)

def undistortRectify(frameR, frameL):

    # Undistort and rectify images
    undistortedL= cv2.remap(frameL, stereoMapL_x, stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
    undistortedR= cv2.remap(frameR, stereoMapR_x, stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)


    return undistortedR, undistortedL
