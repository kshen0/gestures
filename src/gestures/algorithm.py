import cv2
import numpy as np

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
    
    #duplicate the original image
    flow_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    #draw all the flow vectors as lines
    cv2.polylines(flow_image, vectors, 0, (0, 255, 0))
    #draw small circles to indicate lattice points
    for (x1, y1), (x2, y2) in vectors:
        cv2.circle(flow_image, (x1, y1), 1, (0, 255, 0), -1)
    return flow_image