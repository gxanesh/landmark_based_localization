import cv2

# import triangulation as tri
# import calibration

import warnings as warn
warn.filterwarnings("ignore")

# Mediapipe for face detection
import mediapipe as mp
import time
import json
import sys
# sys.path.append('../')
sys.path.append('/usr/local/home/gs37r/Ganesh/Research Project Main/Implementation/landmark_based_localization/stereo_vision_method')
import localization.update_json as update

import stereo_camera_calibration.triangulation as tri
import stereo_camera_calibration.calibration as calib

# import stereo_vision_method.localization.node_localization as nl

# def update_distance(distance, ts = time.time(), filepath ='../localization/data/landmark_data.json'):
#     with open(filepath, 'r') as file:
#         # First we load existing data into a dict.
#         file_data = json.load(file)
#         # Join new_data with file_data inside emp_details
#     file_data["distance"] = distance
#     file_data["timestamp"] = ts
#     # convert back to json.
#     file.close()
#     with open(filepath, "w") as jsonFile:
#         json.dump(file_data, jsonFile, indent=4)
#
#     jsonFile.close()

def get_distance_to_landmark(cam_ids):
    # print("inside calibrated stereo vision module")
    mp_facedetector = mp.solutions.face_detection
    mp_draw = mp.solutions.drawing_utils
    # CamL_id = 0
    # CamR_id = 2
    CamL_id = cam_ids[0]
    CamR_id = cam_ids[1]

    # Open both cameras
    cap_left = cv2.VideoCapture(CamL_id)
    cap_right = cv2.VideoCapture(CamR_id)

    # Stereo vision setup parameters
    frame_rate = 30  # Camera frame rate (maximum at 120 fps)
    B = 10.3  # Distance between the cameras [cm]
    f = 4.4  # Camera lense's focal length [mm]
    alpha = 70  # Camera field of view in the hor# TF_MODEL_URL = 'https://tfhub.dev/google/on_device_vision/classifier/landmarks_classifier_asia_V1/1'
    depths = []

    # Main program loop with face detector and depth estimation using stereo vision
    with mp_facedetector.FaceDetection(min_detection_confidence=0.7) as face_detection:
        # print("test enter")
        while (cap_right.isOpened() and cap_left.isOpened()):

            succes_left, frame_left = cap_left.read()
            succes_right, frame_right = cap_right.read()

            ################## CALIBRATION #########################################################
            # rectify and undistort the captured frames
            # frame_left, frame_right = calib.undistortRectify(frame_left, frame_right)

            #########################################################time.time()###############################

            # If cannot catch any frame, break
            if not succes_left or not  succes_right:
                break
            else:
                start = time.time()
                # Convert the BGR image to RGB
                frame_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2RGB)
                frame_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2RGB)

                # Process the image and find faces
                results_left = face_detection.process(frame_left)
                results_right = face_detection.process(frame_right)

                # Convert the RGB image to BGR
                frame_left = cv2.cvtColor(frame_left, cv2.COLOR_RGB2BGR)
                frame_right = cv2.cvtColor(frame_right, cv2.COLOR_RGB2BGR)

                ################## CALCULATING DEPTH #########################################################

                center_right = 0
                center_left = 0

                if results_right.detections:
                    for id, detection in enumerate(results_right.detections):
                        mp_draw.draw_detection(frame_right, detection)

                        bBox = detection.location_data.relative_bounding_box

                        h, w, c = frame_right.shape

                        boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)

                        center_point_right = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

                        cv2.putText(frame_right, f'{int(detection.score[0] * 100)}%', (boundBox[0], boundBox[1] - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

                if results_left.detections:
                    for id, detection in enumerate(results_left.detections):
                        mp_draw.draw_detection(frame_left, detection)

                        bBox = detection.location_data.relative_bounding_box

                        h, w, c = frame_left.shape

                        boundBox = int(bBox.xmin * w), int(bBox.ymin * h), int(bBox.width * w), int(bBox.height * h)

                        center_point_left = (boundBox[0] + boundBox[2] / 2, boundBox[1] + boundBox[3] / 2)

                        cv2.putText(frame_left, f'{int(detection.score[0] * 100)}%', (boundBox[0], boundBox[1] - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

                # If no ball can be caught in one camera show text "TRACKING LOST"
                if not results_right.detections or not results_left.detections:
                    cv2.putText(frame_right, "Object Tracking Lost", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    cv2.putText(frame_left, "Object Tracking Lost", (75, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                else:
                    # Function to calculate depth of object. Outputs vector of all depths in case of several balls.
                    # All formulas used to find depth is in video presentaion
                    depth = tri.find_depth(center_point_right, center_point_left, frame_right, frame_left, B, f, alpha)
                    depths.append(depth)
                    ts = time.time()

                    cv2.putText(frame_right, "Depth: " + str(round(depth, 1)) + " cm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                (0, 255, 0), 2)
                    cv2.putText(frame_right, "Press "'q'" to close the Window", (20,470),cv2.FONT_HERSHEY_SIMPLEX, 1,
                               (0, 0, 255), 2)
                    cv2.putText(frame_left, "Depth: " + str(round(depth, 1)) + " cm", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2,
                                (0, 255, 0), 2)
                    cv2.putText(frame_left, "Press "'q'" to close the Window", (50,470),cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 255), 2)


                    # Multiply computer value with 205.8 to get real-life depth in [cm]. The factor was found manually.

                    print("Depth: ", str(round(depth, 1))+ "cm")


                end = time.time()
                totalTime = end - start

                fps = 1 / totalTime
                fps = fps/10
                # print("FPS: ", fps)

                cv2.putText(frame_right, f'FPS: {int(fps)}', (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame_left, f'FPS: {int(fps)}', (450, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Show the frames
                cv2.imshow("Stereo right", frame_right)
                cv2.imshow("Stereo left", frame_left)

                # update_json(name=None, distance=None, location=None, ts=None, filepath='./data/landmark_data.json')
                # update.update_json(None, round(depth, 1), None, ts)
                # Hit "q" to close the window
                if (cv2.waitKey(1) & 0xFF == ord('q')):
                    # print(depths)
                    #update the average of the depths captured and current time stamp
                    avg_depth = sum(depths) / len(depths)
                    # update.update_json(distance=round(avg_depth, 1), timestamp=time.time())
                    print("Closing the cameras!")
                    print("Focus the stereo other landmark!")
                    # return avg_depth
                    break

    # Release and destroy all windows before termination
    cap_right.release()
    cap_left.release()

    cv2.destroyAllWindows()
    return avg_depth


# get_distance_to_landmark()
