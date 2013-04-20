#Set to True to show differences between frames instead
#of frames themselves

SHOW_DIFF = False
SHOW_OPTICAL_FLOW = True
USE_HANDTRACKING = False
WIN_NAME = 'Gestures'


#Parameters for Optical Flow Farenback
PYR_SCALE = 0.5
LEVELS = 3
WINSIZE = 15
ITER = 3
POLY_N = 5
POLY_SIGMA = 1.2
FLAGS = 0

#Check to see if we have opencv installed
import sys
try:
    import cv2
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
        #initialize the handtracker
        #self.handtracker = HandTracking()

        #initialize the video window
        cv2.namedWindow(WIN_NAME, cv2.CV_WINDOW_AUTOSIZE)
    
    def start(self):
        #Get 3 successive frames for difference calculation
        frame0 = self.camera.get_frame_gray()
        frame1 = self.camera.get_frame_gray()
        frame2 = self.camera.get_frame_gray()

        while True:
            if SHOW_OPTICAL_FLOW: #Show optical flow field
                if USE_HANDTRACKING: #Use handtracking
                    self.tracker = HandTracking()
                    #get the bounding boxes of the contours
                    print self.tracker.getBoundingBoxes()
                #this single method does the magic of computing the optical flow
                flow = cv2.calcOpticalFlowFarneback(
                        frame0, frame1, 
                        PYR_SCALE, LEVELS, WINSIZE, ITER, POLY_N, POLY_SIGMA, FLAGS)
                image = create_flow(frame1, flow, 10) #create the flow overlay for display
                frame0 = frame1
                frame1 = self.camera.get_frame_gray()
            elif SHOW_DIFF: #Show image difference feed
                image = absdiff(frame0, frame1, frame2)
                frame0 = frame1
                frame1 = frame2
                frame2 = self.camera.get_frame_gray()
            else: #Just show regular webcam feed
                image = frame0
                frame0 = self.camera.get_frame()
            
            self.show_image(image)
            
            #Quit if the user presses ESC
            key = cv2.waitKey(4)
            if key == 27:
                self.stop_gui()
                break

    #Show a GUI with the webcam feed for debugging purposes
    def show_image(self,img):
        cv2.imshow(WIN_NAME, img)
    
    #Stop the webcam
    def stop_gui(self):
        cv2.destroyWindow(WIN_NAME)
    