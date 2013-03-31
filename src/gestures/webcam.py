import sys
try:
    import cv2
except ImportError:
    print 'FATAL: Failed to find opencv'
    sys.exit(1)

class webcam:
    def __init__(self, cam_id=0):
        try:
            self.cam = cv2.VideoCapture(cam_id)
        except Exception,e:
            print 'FATAL: Cannot initialize webcam!'
            sys.exit(1)
        
    def show(self, win_name):
        s, img = self.cam.read()
        
        #create the video window
        cv2.namedWindow(win_name, cv2.CV_WINDOW_AUTOSIZE)
        
        #continue capturing the cam video and show in window
        #until the user presses ESC key
        while s:
            cv2.imshow(win_name, img)
        
            s, img = self.cam.read()
        
            key = cv2.waitKey(10)
            if key == 27:
                cv2.destroyWindow(winName)
            break
        
        print "Goodbye"
        
