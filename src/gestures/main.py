import sys
try:
    import cv2
except ImportError:
    print 'FATAL: Failed to find opencv'
    sys.exit(1)

from webcam import webcam
from algorithm import absdiff
from tools import show_image, stop_gui

SHOW_DIFF = False

def main():
    w = webcam()
    
    #Get 3 successive frames for difference calculation
    t0 = w.get_frame_gray()
    t1 = w.get_frame_gray()
    t2 = w.get_frame_gray()
    
    while True:
        if SHOW_DIFF: #Show image difference feed
            show_image(absdiff(t0, t1, t2))
            t0 = t1
            t1 = t2
            t2 = w.get_frame_gray()
        else: #Just show regular webcam feed
            show_image(t0)
            t0 = w.get_frame()
        
        #Quit if the user presses ESC
        key = cv2.waitKey(10)
        if key == 27:
            stop_gui()
            break
        
if __name__ == '__main__':
    main()