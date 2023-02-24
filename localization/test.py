import json
import numpy as np
def get_node_location():
    '''

    :param landmark_data: landmark json file containing landmark information
    :return: current position of node/camera holder
    '''
    # landamrk_data = {
    # "id": null,
    # "name": [
    # "The Renee and Chaim Gross Foundation",
    # "The Renee and Chaim Gross Foundation"
    # ],
    # "location": [
    # [
    # 40.7285,
    # -73.9988
    # ],
    # [
    # 40.7285,
    # -73.9988
    # ]
    # ],
    # "distance": [
    # 41.1,
    # 39.6
    # ],
    # "timestamp": [
    # 1676236503.2564974,
    # 1676236514.0513842
    # ]
    # }
    # landmark_data =
    # filepath = './data/landmark_data.json'
    # with open(filepath) as json_file:
    #     data = json.load(json_file)
    # # Opening JSON file
    # # with open('data.json') as json_file:
    # # json_file = open(filepath)
    # # landmark_data = json.load(json_file)
    # print(data)

    # landmark_name = landmark_data['name']
    # landmark_location = landmark_data['location']
    # landmark_distance = landmark_data['distance']
    filepath = './data/landmark_data.json'
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


current_position_acc = get_node_location()
print(current_position_acc)
