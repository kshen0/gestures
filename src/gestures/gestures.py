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

import sys
try: import cv2
except ImportError:
    print 'FATAL: Failed to find opencv'
    sys.exit(1)

from algorithm import absdiff, create_flow
from webcam import Webcam
from handtracking import HandTracking


class Gestures():
    def __init__(self):
        #initialize the webcam
        self.camera = Webcam()

        #initialize the video window
        cv2.namedWindow(WIN_NAME, cv2.CV_WINDOW_AUTOSIZE)

        #start collecting frames for processing
        self.initFrames()


    def start(self):
        """Runs image processing loop"""
        while True:
            if USE_HANDTRACKING: 
                pass
            if SHOW_OPTICAL_FLOW: #Show optical flow field
                #this single method does the magic of computing the optical flow
                flow = cv2.calcOpticalFlowFarneback(
                        self.frame0, self.frame1, 
                        PYR_SCALE, LEVELS, WINSIZE, 
                        ITER, POLY_N, POLY_SIGMA, FLAGS)
                image = create_flow(self.frame1, flow, 10) #create the flow overlay for display
            elif SHOW_DIFF: #Show image difference feed
                image = absdiff(frame0, frame1, frame2)
                frame0 = frame1
                frame1 = frame2
                frame2 = self.camera.get_frame_gray()
            else: #Just show regular webcam feed
                image = frame0
                frame0 = self.camera.get_frame()
            
            self.updateFrames()
            self.show_image(image)
            
            #Quit if the user presses ESC
            key = cv2.waitKey(4)
            if key == 27:
                self.stop_gui()
                break


    def initFrames(self):
        """Initiates camera and 3 initial frames for processing"""
        #Get 3 successive frames for difference calculation
        self.img0, self.frame0 = self.camera.get_frame_bgr_and_gray()
        self.img1, self.frame1 = self.camera.get_frame_bgr_and_gray()
        self.img2, self.frame2 = self.camera.get_frame_bgr_and_gray()

        if USE_HANDTRACKING:
            self.initHandTracking()


    def initHandTracking(self):
        """Initiates hand tracker and 3 initial bounding point sets"""
        #Initialize hand tracker
        self.tracker = HandTracking()

        #Get 3 successive sets of bounding points
        self.pts0 = self.tracker.getBoundingPointsArray(self.img0)
        self.pts1 = self.tracker.getBoundingPointsArray(self.img1)
        self.pts2 = self.tracker.getBoundingPointsArray(self.img2)

    
    def updateFrames(self):
        """Updates frames for next loop of processing"""
        #Store old frames
        self.img0 = self.img1
        self.frame0 = self.frame1
        
        #Get new rgb and grayscale frames
        self.img1, self.frame1 = self.camera.get_frame_bgr_and_gray()
        
        #Update set of bounding points
        if USE_HANDTRACKING:
            self.pts0 = self.pts1
            self.pts1 = self.tracker.getBoundingPointsArray(self.img1)


    def show_image(self,img):
        """Show a GUI with the webcam feed for debugging purposes"""
        cv2.imshow(WIN_NAME, img)
    

    def stop_gui(self):
        """Stop the webcam"""
        cv2.destroyWindow(WIN_NAME)
    