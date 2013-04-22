import sys, pdb

try: import cv2
except ImportError:
    print 'FATAL: Failed to find opencv'
    sys.exit(1)

import cv
import numpy as np
from algorithm import absdiff, create_flow, calc_scroll
from webcam import Webcam
from handtracking import HandTracking


#WINDOW PROPERTIES
WIN_NAME = 'Gestures'

#IMAGE PROCESSING
SHOW_OPTICAL_FLOW = True
USE_HANDTRACKING = True
SHOW_DIFF = False

#OPTICAL CACULATION
PYR_SCALE = 0.5
LEVELS = 3
WINSIZE = 15
ITER = 3
POLY_N = 5
POLY_SIGMA = 1.2
FLAGS = 0


class Gestures():
    def __init__(self):
        #initialize the webcam
        self.camera = Webcam()

        #initialize the video window
        cv2.namedWindow(WIN_NAME, cv2.CV_WINDOW_AUTOSIZE)

        #start collecting frames for processing
        self.init_frames()


    def start(self):
        """Runs image processing loop"""
        while True:
            if SHOW_OPTICAL_FLOW: #Show optical flow field
                #this single method does the magic of computing the optical flow
                #flow = cv2.calcOpticalFlowFarneback(
                        #self.frame0, 
                        #self.frame1, 
                        #PYR_SCALE, 
                        #LEVELS, 
                        # WINSIZE, 
                        # ITER, 
                        # POLY_N, 
                        # POLY_SIGMA, 
                        # FLAGS)
                pass
                #image = create_flow(self.frame1, flow, 10) #create the flow overlay for display
            elif SHOW_DIFF: #Show image difference feed
                image = absdiff(self.frame0, self.frame1, self.frame2)
                self.frame0 = self.frame1
                self.frame1 = self.frame2
                self.frame2 = self.camera.get_frame_gray()
            else: #Just show regular webcam feed
                image = self.frame0
                self.frame0 = self.camera.get_frame()
            
            self.update_frames()
            #self.show_image(image)

            # send scroll event
            calc_scroll(self.dir)
            
            key = cv2.waitKey(4)
            if key == 27: 
                #Quit if the user presses ESC
                self.stop_gui()
                break
            if key == 100: 
                #Toggle hand tracking debug window
                self.tracker.toggle_debug()
                


    def init_frames(self):
        """Initiates camera and 3 initial frames for processing"""
        #Get 3 successive frames for difference calculation
        self.img0, self.frame0 = self.camera.get_frame_bgr_and_gray()
        self.img1, self.frame1 = self.camera.get_frame_bgr_and_gray()
        self.img2, self.frame2 = self.camera.get_frame_bgr_and_gray()

        if USE_HANDTRACKING:
            self.init_hand_tracking()


    def init_hand_tracking(self):
        """Initiates hand tracker and 3 initial bounding point sets"""
        #Initialize hand tracker
        self.tracker = HandTracking()

        #Get 3 successive sets of features (feature: array of points)
        #Each feature array is based on a frame's bounding boxes 
        #and indicates the areas for which optical flow should be calculated
        self.mpts0 = self.tracker.getBoundingMidpoints(self.img0)
        self.mpts1 = self.tracker.getBoundingMidpoints(self.img1)
        self.mpts2 = self.tracker.getBoundingMidpoints(self.img2)
        

    def update_frames(self):
        """Updates frames for next loop of processing"""
        #Store old frames
        self.img0 = self.img1
        self.frame0 = self.frame1
        
        #Get new rgb and grayscale frames
        self.img1, self.frame1 = self.camera.get_frame_bgr_and_gray()
        
        #Update bounding arrays
        if USE_HANDTRACKING:
            self.mpts0 = self.mpts1
            self.mpts1 = self.tracker.getBoundingMidpoints(self.img1)
            self.dir = self.get_direction_vector()
            self.tracker.update_dir_data(self.dir)


    def get_direction_vector(self):
        """Calculates the vector between the midpoints of bounding boxes."""
        if len(self.mpts0) is not len(self.mpts1):
            return

        diffs = []
        for i in range(len(self.mpts0)): 
            mp0 = self.mpts0[i]
            mp1 = self.mpts1[i]
            diff = [a - b for a, b in zip(mp1, mp0)]
            dist = np.sqrt(diff[0]**2+diff[1]**2)
            diffs.append((diff, dist))
            
        if len(diffs) == 0:
            return None 

        return max(diffs, key=lambda a: a[1])


    def show_image(self,img):
        """Show a GUI with the webcam feed for debugging purposes"""
        cv2.imshow(WIN_NAME, img)


    def stop_gui(self):
        """Stop the webcam"""
        cv2.destroyWindow(WIN_NAME)
    
