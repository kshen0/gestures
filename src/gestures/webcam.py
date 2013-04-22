import sys
import cv2
import numpy as np

class Webcam:
    #Constructor. cam_id is usually 0 but if you have more
    #than 1 webcam, it might be something else 
    def __init__(self, cam_id=0):
        #attempt to connect to the webcam
        try:
            self.cam = cv2.VideoCapture(cam_id)
        except Exception:
            print 'FATAL: Cannot initialize webcam!'
            sys.exit(1)
        
        self.width = 640
        self.height = 480

        #Camera resolution
        self.cam.set(3,self.width)
        self.cam.set(4,self.height)

    
    #Gets a single frame from the camera. returns a tuple
    #(s, img) with s a flag indicating success or not and img
    # the image.
    def get_frame(self):
        return self.cam.read()[1]
    

    #Same get_frame except grayscale image
    def get_frame_gray(self):
        return cv2.cvtColor(self.get_frame(), cv2.COLOR_BGR2GRAY)


    #Return both BGR and grayscale images
    def get_frame_bgr_and_gray(self):
        img = self.get_frame()
        return (img, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))        


    #processes the frame within the rectangles
    def crop_frame(x, y, width, height):
        print "blah"