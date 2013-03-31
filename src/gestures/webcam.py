import sys
import cv2

class webcam:
    def __init__(self, cam_id=0, win_name = 'Webcam'):
        #attempt to connect to the webcam
        try:
            self.cam = cv2.VideoCapture(cam_id)
        except Exception,e:
            print 'FATAL: Cannot initialize webcam!'
            sys.exit(1)
    
    #Gets an single frame from the camera. returns a tuple
    #(s, img) with s a flag indicating success or not and img
    # the image.
    def get_frame(self):
        return self.cam.read()[1]
    
    #Same get_frame except grayscale image
    def get_frame_gray(self):
        return cv2.cvtColor(self.cam.read()[1], cv2.COLOR_RGB2GRAY)
    

        
