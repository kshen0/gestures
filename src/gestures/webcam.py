import sys
import cv2
import numpy as np

class Webcam:
    
    def __init__(self, cam_id=0):
        """
        Constructor. cam_id is usually 0 but if you have more
        than 1 webcam, it might be something else 
        """
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

    
    def get_frame(self):
        """
        Gets a single frame from the camera. returns a tuple
        (s, img) with s a flag indicating success or not and img
        the image.
        """
        return self.cam.read()[1]
    

    def get_frame_gray(self):
        """Same get_frame except grayscale image"""
        return cv2.cvtColor(self.get_frame(), cv2.COLOR_BGR2GRAY)


    def get_frame_bgr_and_gray(self):
        """Return both BGR and grayscale images"""
        img = self.get_frame()
        return (img, cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))        
