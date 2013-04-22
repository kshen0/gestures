import cv2
import numpy as np
import scrolling as scroll
import time
import math

#Computes the absolute grayscale difference given 3 successive images
#This detects "movements" in the video
def absdiff(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

#Creates a vector field image based on optical flow data
def create_flow(image, flow, step_size=16):
    #create a lattice and find the flow vector at each lattice point
    #we will be drawing these vectors. step_size determines lattice density
    height, width = image.shape[:2]
    y, x = np.mgrid[step_size/2:height:step_size, step_size/2:width:step_size].reshape(2,-1)
    fx, fy = flow[y,x].T
    vectors = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    vectors = np.int32(vectors + 0.5)
    #print flow
    #duplicate the original image
    flow_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    #draw all the flow vectors as lines
    cv2.polylines(flow_image, vectors, 0, (0, 255, 0))
    #draw small circles to indicate lattice points
    for (x1, y1), (x2, y2) in vectors:
        cv2.circle(flow_image, (x1, y1), 1, (0, 255, 0), -1)
    #average_flow(flow)
    return flow_image

#calculates the average flow direction of the vectors
"""
def average_flow(flow):
    #make changes to flow so that only vertical information is preserved
    vectors = []
    for f1 in flow:
        for f2 in f1:
            vectors.append(f2[1])
    result = np.average(vectors)
    return result
"""

def calc_scroll(dir_vector):
    if not dir_vector:
        return

    x = dir_vector[0][0]
    y = dir_vector[0][1]
    magnitude = dir_vector[1]
    if x != 0:
        print y/x, magnitude
    if (x == 0 or abs(y / x) > 3) and magnitude > 100:
        speed = min(6, magnitude / 10)
        direction = math.copysign(1, y)
        scroll.scroll_wheel(speed, direction, 50)
    #print vectors
    """
    if result > 1.0:
        print "Strong DOWN"
        scroll.scroll_wheel_down(50)
    elif result > 0.2:
        print "Weak DOWN"
        scroll.scroll_wheel_down(30)
    elif result < -1.0:
        print "Strong UP"
        scroll.scroll_wheel_up(50)
    elif result < -1.0:
        print "Weak UP"
        scroll.scroll_wheel_up(30)

    """