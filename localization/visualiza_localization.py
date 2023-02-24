import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
plt.style.use('seaborn-poster')


def visualize_node_localization(landmark_XCoords,landmark_YCoords,current_position_acc):
    plt.figure(figsize = (10,10))
    plt.plot(landmark_XCoords, landmark_YCoords, 'r^')
    for x,y in zip(landmark_XCoords, landmark_YCoords):

        label = f"({x},{y})"

        plt.annotate(label, # this is the text
                     (x,y), # these are the coordinates to position the label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center') # horizontal alignment can be left, right or center
    plt.scatter(current_position_acc[0], current_position_acc[1], s=200)
    # text is right-aligned
    # plt.text(current_position_acc[0], current_position_acc[1],'{},{}'.format(current_position_acc[0].round(2),current_position_acc[1].round(2)))
    node_label = f"({current_position_acc[0][0].round(2)},{current_position_acc[1][0].round(2)})"
    plt.annotate(node_label, # this is the text
                     (current_position_acc[0][0],current_position_acc[1][0]), # these are the coordinates to position the label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center')
    # plt.plot(landmark_XCoords, alpha[0]*landmark_XCoords + alpha[1], 'r')


    # draw line between node and landmarks
    # x, y = [X_Coords,Y_Coords]
    x1,y1 = [current_position_acc[0][0].round(2),landmark_XCoords[0]],[current_position_acc[1][0].round(2),landmark_YCoords[0]]
    x2,y2 = [current_position_acc[0][0].round(2),landmark_XCoords[1]],[current_position_acc[1][0].round(2),landmark_YCoords[1]]
    x3,y3 = [current_position_acc[0][0].round(2),landmark_XCoords[2]],[current_position_acc[1][0].round(2),landmark_YCoords[2]]
    plt.plot(x1,y1,color = 'gray')
    plt.plot(x2,y2,color = 'gray')
    plt.plot(x3,y3,color = 'gray')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
