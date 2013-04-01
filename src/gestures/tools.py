import sys
import cv2

WIN_NAME = 'Webcam feed'

#initialize the video window
cv2.namedWindow(WIN_NAME, cv2.CV_WINDOW_AUTOSIZE)

#Show a GUI with the webcam feed for debugging purposes
def show_image(img):
    cv2.imshow(WIN_NAME, img)

#Stop the webcam
def stop_gui():
    cv2.destroyWindow(WIN_NAME)