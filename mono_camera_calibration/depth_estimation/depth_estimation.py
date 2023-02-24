

def avgDepth(imgLeft,imgRight,bSize):
    depthMap  = ShowDisparity(imgLeft,imgRight,bSize)
    avg_depth, _ = cv2.meanStdDev(depthMap)
    return avg_depth


def avgDepths(imgLeft,imgRight,block_size_range):
    avg_depths = []
    for bSize in block_size_range:
        avg_depth = avgDepth(imgLeft,imgRight,bSize)
        avg_depths.append(avg_depth[0][0].round(2))
    return avg_depths

